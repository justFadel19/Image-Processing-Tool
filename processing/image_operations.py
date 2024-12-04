import numpy as np
from PIL import Image

def add_image_and_copy(image):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Convert image to numpy array
    img_array = np.array(image, dtype=np.float32)
    
    # Add the image with itself
    result = img_array + img_array
    
    # Clip values to valid range
    result = np.clip(result, 0, 255).astype(np.uint8)
    return Image.fromarray(result)

def subtract_image_and_copy(image):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Convert image to numpy array
    img_array = np.array(image, dtype=np.float32)
    
    # Create a brighter version by multiplying
    bright_version = img_array * 1.5
    
    # Subtract the original from the bright version
    result = bright_version - img_array
    
    # Clip values to valid range
    result = np.clip(result, 0, 255).astype(np.uint8)
    return Image.fromarray(result)

def invert_image(image):
    # Handle both RGB and grayscale images
    if image.mode == 'RGB':
        # Convert image to numpy array
        img_array = np.array(image)
        # Invert each channel
        inverted = 255 - img_array
        return Image.fromarray(inverted.astype(np.uint8), 'RGB')
    else:
        # Convert to grayscale if not already
        if image.mode != 'L':
            image = image.convert('L')
        # Convert to numpy array and invert
        img_array = np.array(image)
        inverted = 255 - img_array
        return Image.fromarray(inverted.astype(np.uint8), 'L')
