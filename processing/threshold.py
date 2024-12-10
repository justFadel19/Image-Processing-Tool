from PIL import Image

def calculate_threshold(image):
    """
    Converts an image to grayscale if it isn't already, calculates a global threshold
    based on the average pixel value, and applies the threshold to create a binary image.

    Args:
        image (PIL.Image.Image): The input image to be thresholded.

    Returns:
        PIL.Image.Image: The thresholded binary image.
    """
    
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size
    
    # Calculate the average pixel value (global threshold)
    pixel_values = [image.getpixel((x, y)) for x in range(width) for y in range(height)]
    threshold = sum(pixel_values) // len(pixel_values)
    print(f"Calculated Threshold: {threshold}")
    
    # Return the original image and the calculated threshold
    return image