import numpy as np
from PIL import Image

def normalize_output(image_array):
    """Normalize the output to 0-255 range"""
    min_val = np.min(image_array)
    max_val = np.max(image_array)
    if max_val == min_val:
        return np.zeros_like(image_array, dtype=np.uint8)
    return np.uint8(255 * (image_array - min_val) / (max_val - min_val))

def homogeneity_operator(image):
    """
    Apply the Homogeneity Operator for edge detection.
    
    Args:
        image (PIL.Image.Image): The input grayscale image.
    
    Returns:
        PIL.Image.Image: The edge-detected image.
    """
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size
    img_array = np.array(image, dtype=np.float32)

    # Prepare an array for the output
    edge_img = np.zeros_like(img_array)

    # Define the neighbor offsets
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    # Apply the homogeneity operator
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            pixel = img_array[y, x]
            differences = [abs(pixel - img_array[y + dy, x + dx]) for dx, dy in neighbors]
            edge_img[y, x] = max(differences)

    # Normalize the output to 0-255 range
    edge_img = normalize_output(edge_img)

    return Image.fromarray(edge_img)

def difference_operator(image):
    """
    Apply the Difference Operator for edge detection.
    
    Args:
        image (PIL.Image.Image): The input grayscale image.
    
    Returns:
        PIL.Image.Image: The edge-detected image.
    """
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size
    img_array = np.array(image, dtype=np.float32)

    # Prepare an array for the output
    edge_img = np.zeros_like(img_array)

    # Define the neighbor offsets for horizontal and vertical differences
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Apply the difference operator
    for y in range(1, height-1):
        for x in range(1, width-1):
            pixel = img_array[y, x]
            differences = [abs(pixel - img_array[y + dy, x + dx]) for dx, dy in neighbors]
            edge_img[y, x] = sum(differences) // len(differences)

    # Normalize the output to 0-255 range
    edge_img = normalize_output(edge_img)

    return Image.fromarray(edge_img)

def gaussian_kernel(size, sigma):
    """Create a Gaussian kernel"""
    kernel = np.zeros((size, size), dtype=np.float32)
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
    
    return kernel

def apply_gaussian(image_array, kernel):
    """Apply Gaussian filter manually"""
    height, width = image_array.shape
    k_size = kernel.shape[0]
    pad = k_size // 2
    padded = np.pad(image_array, ((pad, pad), (pad, pad)), mode='reflect')
    output = np.zeros_like(image_array)
    
    for i in range(height):
        for j in range(width):
            window = padded[i:i + k_size, j:j + k_size]
            output[i, j] = np.sum(window * kernel)
    
    return output

def difference_of_gaussians(image, sigma1=1.0, sigma2=2.0, size=5):
    """Edge detection using difference of Gaussians"""
    if image.mode != 'L':
        image = image.convert('L')
    
    img_array = np.array(image, dtype=np.float32)
    
    # Create Gaussian kernels
    g1 = gaussian_kernel(size, sigma1)
    g2 = gaussian_kernel(size, sigma2)
    
    # Apply Gaussians
    smooth1 = apply_gaussian(img_array, g1)
    smooth2 = apply_gaussian(img_array, g2)
    
    # Calculate difference
    output = np.abs(smooth1 - smooth2)
    
    return Image.fromarray(normalize_output(output))

def contrast_based_edge_detection(image, kernel_size=3):
    """Edge detection based on local contrast"""
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size
    img_array = np.array(image, dtype=np.float32)
    pad = kernel_size // 2
    
    # Create padded image
    padded = np.pad(img_array, ((pad, pad), (pad, pad)), mode='reflect')
    
    # Output array
    output = np.zeros((height, width), dtype=np.float32)
    
    # Apply contrast operation
    for y in range(height):
        for x in range(width):
            window = padded[y:y + kernel_size, x:x + kernel_size]
            center_value = window[pad, pad]
            mean_value = np.mean(window)
            output[y, x] = abs(center_value - mean_value)
    
    return Image.fromarray(normalize_output(output))

def variance_operator(image, kernel_size=3):
    """Edge detection based on local variance"""
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size
    img_array = np.array(image, dtype=np.float32)
    pad = kernel_size // 2
    
    # Create padded image
    padded = np.pad(img_array, ((pad, pad), (pad, pad)), mode='reflect')
    
    # Output array
    output = np.zeros((height, width), dtype=np.float32)
    
    # Apply variance operation
    for y in range(height):
        for x in range(width):
            window = padded[y:y + kernel_size, x:x + kernel_size]
            output[y, x] = np.var(window)
    
    return Image.fromarray(normalize_output(output))

def range_operator(image, kernel_size=3):
    """Edge detection based on local range of intensities"""
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size
    img_array = np.array(image, dtype=np.float32)
    pad = kernel_size // 2
    
    # Create padded image
    padded = np.pad(img_array, ((pad, pad), (pad, pad)), mode='reflect')
    
    # Output array
    output = np.zeros((height, width), dtype=np.float32)
    
    # Apply range operation
    for y in range(height):
        for x in range(width):
            window = padded[y:y + kernel_size, x:x + kernel_size]
            output[y, x] = np.max(window) - np.min(window)
    
    return Image.fromarray(normalize_output(output))