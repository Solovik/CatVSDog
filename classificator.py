import tensorflow as tf
from PIL import Image
import numpy as np

def load_tf_model(path: str) -> tf.keras.Model:
    """
    Load serialized keras model from the directory `path`

    :param path: directory with serialized keras model
    :return: serialized keras model
    """
    print(f"Loading keras model from {path}")
    return tf.keras.models.load_model(path)


def is_cat(model: tf.keras.Model, img: Image) -> bool:
    """
    Returns True if Cat on the picture, Dog otherwise

    :param model: Loaded model for CatVSDog classification
    :param img: PIL PNG image with size 224x224
        example:
        >>> print(img)
        <PIL.PngImagePlugin.PngImageFile image mode=RGB size=224x224 at ...>
    :return:
    """
    img_array = tf.cast(tf.keras.utils.img_to_array(img), tf.float32) / 255.0
    img_expended = np.expand_dims(img_array, axis=0)
    return model.predict(img_expended)[0][0] < 0.5
