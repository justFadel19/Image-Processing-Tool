import numpy as np
from PIL import Image

def apply_threshold(image):
    grayscale = image.convert("L")
    image_array = np.array(grayscale)
    threshold_value = np.mean(image_array)
    thresholded_array = (image_array > threshold_value) * 255
    thresholded_image = Image.fromarray(np.uint8(thresholded_array))
    return thresholded_image
