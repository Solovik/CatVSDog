import argparse
import logging as log
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from time import time
from PIL import Image
from pathlib import Path

from classificator import load_tf_model, is_cat

log.basicConfig(filename="flow.log", level=log.DEBUG)
log.getLogger().addHandler(log.StreamHandler(sys.stdout))

output_dir = 'data/output'

class Classificator:
    lock = Lock()

    def __init__(self):
        st = time()
        self.model = load_tf_model('model')
        log.info(f'Model loaded in: {time() - st} s')

    def cat_or_other(self, img) -> bool:
        with self.lock:
            return is_cat(self.model, img)


class Statistics:
    # количество скачанных файлов, количество скачанных байт,
    # количество запросов завершившихся с ошибкой, процент котиков, процент собачек, общее время выполнения.
    lock = Lock()
    Downloaded_Files = 'downloaded_files'
    Downloaded_Bytes = 'downloaded_bytes'
    Total_Requests = 'total_requests'
    Failed_requests = 'failed_requests'
    Cat_Counts = 'cat_counts'
    Total_Time = 'total_time'

    def __init__(self):
        self.stat = {type(self).Downloaded_Files: 0,
                     type(self).Downloaded_Bytes: 0,
                     type(self).Total_Requests: 0,
                     type(self).Failed_requests: 0,
                     type(self).Cat_Counts: 0,
                     type(self).Total_Time: 0}

    def increase(self, name, count=1.0):
        with self.lock:
            self.stat[name] += count

    def __str__(self):
        return f'Total tasks: {int(self.stat[self.Total_Requests])}\n' \
               f'Total time: {self.stat[self.Total_Time]} s\n' \
               f'Total download: {int(self.stat[self.Downloaded_Files])}\n' \
               f'Total bytes: {self.stat[self.Downloaded_Bytes]} bytes\n' \
               f'Failed: {int(self.stat[self.Failed_requests])}\n' \
               f'Cats %: {float(self.stat[self.Cat_Counts])/self.stat[self.Downloaded_Files]*100}%\n' \
               f'Dogs %: {float(self.stat[self.Downloaded_Files]-self.stat[self.Cat_Counts])/self.stat[self.Downloaded_Files]*100}%'


def parse_input_params():
    parser = argparse.ArgumentParser(
        prog='CatsVsDogs',
        description='Sort images into dogs/cats dirs',
        epilog='Text at the bottom of help')
    parser.add_argument('urlsFile')
    parser.add_argument('-t', '--threads', default=1, type=int)

    args = parser.parse_args()

    return args


def create_tasks(file: str, classificator: Classificator, stat: Statistics):
    tasks = []
    with open(file) as file:
        for ur in file.readlines():
            tasks.append((ur.strip(), classificator, stat))

    return list(enumerate(tasks))


def task(task):
    print(f'Task {task[0]}:{task[1][0]}')
    task[1][2].increase(Statistics.Total_Requests)

    try:
        with urllib.request.urlopen(task[1][0]) as src:
            imgSize = src.headers['content-length']
            log.info(f"Downloaded image: {task[0]}. Size:{imgSize}. URL:{task[1][0]}")
            resizedImg = Image.open(src).resize((224, 224)).convert("RGB")

            st = time()
            isCat = task[1][1].cat_or_other(resizedImg)
            log.info(f'Time checking cat: {time() - st}')

            task[1][2].increase(Statistics.Downloaded_Files)
            task[1][2].increase(Statistics.Downloaded_Bytes, int(imgSize))
            if isCat:
                task[1][2].increase(Statistics.Cat_Counts)
                resizedImg.save(f'{output_dir}/cats/{str(task[0]).rjust(5, "0")}.png')
            else:
                resizedImg.save(f'{output_dir}/dogs/{str(task[0]).rjust(5, "0")}.png')

            log.info(f"Processed image: {task[0]}. {isCat} Size:{imgSize}. URL:{task[1][0]}")
    except Exception as e:
        task[1][2].increase(Statistics.Failed_requests)
        log.info(f"FAILED to process. Image: {task[0]}. URL:{task[1][0]}. Error: {str(e)}")


def run():
    Path(f"{output_dir}/cats").mkdir(parents=True, exist_ok=True)
    Path(f"{output_dir}/dogs").mkdir(parents=True, exist_ok=True)

    args = parse_input_params()
    log.info(f'{args}')

    st = time()
    classificator = Classificator()
    print(f'Classificator loaded in {time() - st} s')

    stat = Statistics()

    tasks = create_tasks(args.urlsFile, classificator, stat)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(task, tasks)

    stat.increase(Statistics.Total_Time, time() - st)

    log.info(f'Statistics:\n{stat}')


if __name__ == '__main__':
    run()

# Model loaded in: 6.615522861480713 s
# Classificator loaded in 6.615522861480713 s

# 4 threads
# Statistics:
# Total tasks: 7
# Total time: 9.357143640518188 s
# Total download: 6
# Total bytes: 2175837 bytes
# Failed: 1
# Cats %: 50.0%
# Dogs %: 50.0%

# 1 thread
# Statistics:
# Total tasks: 7
# Total time: 12.566015005111694 s
# Total download: 6
# Total bytes: 2175837 bytes
# Failed: 1
# Cats %: 50.0%
# Dogs %: 50.0%