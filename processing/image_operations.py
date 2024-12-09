import numpy as np
from PIL import Image

def add_image_and_copy(image):
    """
    Add the image with itself and return the result.
    
    Args:
        image (PIL.Image.Image): The input image to be processed.
    
    Returns:
        PIL.Image.Image: The image with the addition operation applied.
    """
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size
    img_array = np.array(image, dtype=np.float32)
    
    # Add the image with itself
    result = np.zeros_like(img_array)
    for y in range(height):
        for x in range(width):
            result[y, x] = img_array[y, x] + img_array[y, x]
    
    # Clip values to valid range
    for y in range(height):
        for x in range(width):
            if result[y, x] > 255:
                result[y, x] = 255
            elif result[y, x] < 0:
                result[y, x] = 0
    
    return Image.fromarray(result.astype(np.uint8))

def subtract_image_and_copy(image):
    """
    Subtract the original image from a brighter version and return the result.
    
    Args:
        image (PIL.Image.Image): The input image to be processed.
    
    Returns:
        PIL.Image.Image: The image with the subtraction operation applied.
    """
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size
    img_array = np.array(image, dtype=np.float32)
    
    # Create a brighter version by multiplying
    bright_version = np.zeros_like(img_array)
    for y in range(height):
        for x in range(width):
            bright_version[y, x] = img_array[y, x] * 1.5
    
    # Subtract the original from the bright version
    result = np.zeros_like(img_array)
    for y in range(height):
        for x in range(width):
            result[y, x] = bright_version[y, x] - img_array[y, x]
    
    # Clip values to valid range
    for y in range(height):
        for x in range(width):
            if result[y, x] > 255:
                result[y, x] = 255
            elif result[y, x] < 0:
                result[y, x] = 0
    
    return Image.fromarray(result.astype(np.uint8))

def invert_image(image):
    """
    Invert the colors of the image and return the result.
    
    Args:
        image (PIL.Image.Image): The input image to be processed.
    
    Returns:
        PIL.Image.Image: The image with the inversion operation applied.
    """
    # Handle both RGB and grayscale images
    if image.mode == 'RGB':
        width, height = image.size
        img_array = np.array(image)
        inverted = np.zeros_like(img_array)
        
        # Invert each channel
        for y in range(height):
            for x in range(width):
                for c in range(3):  # RGB channels
                    inverted[y, x, c] = 255 - img_array[y, x, c]
        
        return Image.fromarray(inverted.astype(np.uint8), 'RGB')
    else:
        # Convert to grayscale if not already
        if image.mode != 'L':
            image = image.convert('L')
        
        width, height = image.size
        img_array = np.array(image)
        inverted = np.zeros_like(img_array)
        
        # Invert the grayscale image
        for y in range(height):
            for x in range(width):
                inverted[y, x] = 255 - img_array[y, x]
        
        return Image.fromarray(inverted.astype(np.uint8), 'L')