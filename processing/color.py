from PIL import Image


def convert_to_grayscale(image):
    return image.convert("L")
