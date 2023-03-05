from unittest import TestCase
from catsVSdogs import create_tasks

class CatsVsDogsTest(TestCase):
    
    def test_create_tasks(self):
        urls = 'data/input/urllist.txt'
        tasks = create_tasks(urls, None, None)

        expected = [(0, ('https://images6.alphacoders.com/337/337780.jpg', None, None)),
                    (1, ('https://images.unsplash.com/photo-1600352712371-15fd49ca42b5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8Nnx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=60', None, None)),
                    (2, ('https://www.shutterstock.com/image-photo/beautiful-white-kitten-on-background-260nw-118955326.jpg', None, None)),
                    (3, ('https://images.unsplash.com/photo-1616781296073-65d3f087de41?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8OHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=60', None, None)),
                    (4, ('https://images.unsplash.com/photo-1583083527882-4bee9aba2eea?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8OHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=60', None, None)),
                    (5, ('https://mobimg.b-cdn.net/v3/fetch/c8/c8cc29813c65d8b09742b0bc3337b2d2.jpeg', None, None)),
                    (6, ('https://1dens.files.wordpress.com/2013/10/cute-cats-068.jpg', None, None))]

        self.assertEqual(expected, tasks)