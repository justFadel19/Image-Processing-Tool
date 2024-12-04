import numpy as np
from PIL import Image

def simple_halftone(image):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Convert to array and calculate threshold
    img_array = np.array(image)
    threshold_value = np.mean(img_array)
    
    # Apply threshold
    halftone_array = np.where(img_array > threshold_value, 255, 0).astype(np.uint8)
    return Image.fromarray(halftone_array)

def error_diffusion_halftoning(image, threshold=128):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')

    # Convert the image into a NumPy array
    img_array = np.array(image, dtype=np.float32)  # Use float to handle errors

    # Get dimensions of the image
    height, width = img_array.shape

    # Process each pixel in the image
    for y in range(height):
        for x in range(width):
            old_pixel = img_array[y, x]
            new_pixel = 255 if old_pixel >= threshold else 0  # Thresholding
            img_array[y, x] = new_pixel  # Update the pixel

            # Calculate the error
            error = old_pixel - new_pixel

            # Propagate the error to neighbors (Floyd-Steinberg)
            if x + 1 < width:
                img_array[y, x + 1] += error * 7 / 16
            if y + 1 < height and x > 0:
                img_array[y + 1, x - 1] += error * 3 / 16
            if y + 1 < height:
                img_array[y + 1, x] += error * 5 / 16
            if y + 1 < height and x + 1 < width:
                img_array[y + 1, x + 1] += error * 1 / 16

    # Clip values to be between 0 and 255
    img_array = np.clip(img_array, 0, 255)

    # Convert back to a PIL image and return
    return Image.fromarray(img_array.astype(np.uint8))