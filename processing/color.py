from PIL import Image
import numpy as np


def convert_to_grayscale(image):
    """
    Convert an image to grayscale using manual computation of pixel values with standard luminance weights.
    
    Args:
        image: PIL Image object to convert to grayscale.
        
    Returns:
        PIL Image: The grayscale version of the input image.
    """
    # Ensure image is in RGB mode
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    width, height = image.size
    
    # Create a new image for the grayscale result
    grayscale_img = Image.new("L", (width, height))
    
    # Process each pixel
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            # Calculate grayscale value using standard luminance weights
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            grayscale_img.putpixel((x, y), gray)
    
    return grayscale_img
