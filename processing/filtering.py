import numpy as np
from PIL import Image

def convolve(image_array, kernel):
    kernel_height, kernel_width = kernel.shape
    image_height, image_width = image_array.shape
    output = np.zeros_like(image_array)

    # Use reflect padding for better edge handling
    padded_image = np.pad(image_array, 
                         ((kernel_height // 2, kernel_height // 2),
                          (kernel_width // 2, kernel_width // 2)), 
                         mode="reflect")

    for i in range(image_height):
        for j in range(image_width):
            region = padded_image[i:i + kernel_height, j:j + kernel_width]
            output[i, j] = np.sum(region * kernel)

    return output

def apply_highpass(image):
    """
    Apply a high-pass filter to an image.
    
    Args:
        image (PIL.Image.Image): The input image to be processed.

    Returns:
        PIL.Image.Image: The image with high-pass filter applied.
    """
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Convert to array
    image_array = np.array(image, dtype=np.float64)
    
    # High-pass filter mask (Laplacian)
    highpass_mask = np.array([[-1, -1, -1],
                              [-1,  9, -1],
                              [-1, -1, -1]])
    
    # Apply convolution
    filtered = convolve(image_array, highpass_mask)
    filtered = np.clip(filtered, 0, 255).astype(np.uint8)
    
    return Image.fromarray(filtered)

def apply_lowpass(image):
    """
    Apply a low-pass filter to an image.
    
    Args:
        image (PIL.Image.Image): The input image to be processed.

    Returns:
        PIL.Image.Image: The image with low-pass filter applied.
    """
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size
    image_array = np.array(image, dtype=np.float64)
    
    # Gaussian kernel
    size = 5
    sigma = 1.0
    kernel = np.zeros((size, size), dtype=np.float64)
    center = size // 2
    sum_val = 0.0
    
    for i in range(size):
        for j in range(size):
            x = i - center
            y = j - center
            kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
            sum_val += kernel[i, j]
    
    # Normalize the kernel
    for i in range(size):
        for j in range(size):
            kernel[i, j] /= sum_val
    
    # Apply convolution
    filtered = convolve(image_array, kernel)
    filtered = np.clip(filtered, 0, 255).astype(np.uint8)
    
    return Image.fromarray(filtered)

def apply_median(image, size=5):
    """
    Apply a median filter to an image.
    
    Args:
        image (PIL.Image.Image): The input image to be processed.
        size (int): The size of the median filter.

    Returns:
        PIL.Image.Image: The image with median filter applied.
    """
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size
    image_array = np.array(image, dtype=np.float64)
    
    # Prepare an array for the output
    filtered = np.zeros_like(image_array)
    
    # Apply median filter
    pad = size // 2
    padded_image = np.pad(image_array, pad, mode='reflect')
    
    for i in range(height):
        for j in range(width):
            window = padded_image[i:i + size, j:j + size]
            median_value = np.median(window)
            filtered[i, j] = median_value
    
    filtered = np.clip(filtered, 0, 255).astype(np.uint8)
    
    return Image.fromarray(filtered)