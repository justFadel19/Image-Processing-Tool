import numpy as np
from PIL import Image
from scipy.ndimage import median_filter, gaussian_filter

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
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Convert to array
    image_array = np.array(image, dtype=np.float64)
    
    # Apply Gaussian filter for better smoothing
    filtered = gaussian_filter(image_array, sigma=1)
    
    # Ensure proper range
    filtered = np.clip(filtered, 0, 255).astype(np.uint8)
    
    return Image.fromarray(filtered)

def apply_median(image, size=5):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Convert to array
    image_array = np.array(image)
    
    # Apply median filter using scipy
    # Increased size to 5x5 for better noise reduction
    filtered = median_filter(image_array, size=size)
    
    return Image.fromarray(filtered.astype(np.uint8))
