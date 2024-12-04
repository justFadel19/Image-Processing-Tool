import numpy as np
from PIL import Image

def normalize_output(image_array):
    """Normalize the output to 0-255 range"""
    min_val = np.min(image_array)
    max_val = np.max(image_array)
    if max_val == min_val:
        return np.zeros_like(image_array, dtype=np.uint8)
    return np.uint8(255 * (image_array - min_val) / (max_val - min_val))

def apply_window_operation(image, kernel_size, operation):
    """Apply a window operation with proper padding"""
    if image.mode != 'L':
        image = image.convert('L')
    
    # Convert to array
    image_array = np.array(image, dtype=np.float32)
    height, width = image_array.shape
    pad = kernel_size // 2
    
    # Create padded image
    padded = np.pad(image_array, ((pad, pad), (pad, pad)), mode='reflect')
    
    # Output array
    output = np.zeros((height, width), dtype=np.float32)
    
    # Apply operation to each window
    for i in range(height):
        for j in range(width):
            window = padded[i:i + kernel_size, j:j + kernel_size]
            output[i, j] = operation(window)
    
    return normalize_output(output)

def homogeneity_operator(image, kernel_size=3):
    """Edge detection based on intensity range in local window"""
    def homogeneity_op(window):
        return np.max(window) - np.min(window)
    
    output = apply_window_operation(image, kernel_size, homogeneity_op)
    return Image.fromarray(output)

def difference_operator(image):
    """Simple horizontal and vertical difference operator"""
    if image.mode != 'L':
        image = image.convert('L')
    
    img_array = np.array(image, dtype=np.float32)
    height, width = img_array.shape
    
    # Calculate horizontal and vertical differences
    h_diff = np.zeros_like(img_array)
    v_diff = np.zeros_like(img_array)
    
    # Horizontal differences
    h_diff[:, :-1] = np.abs(img_array[:, 1:] - img_array[:, :-1])
    
    # Vertical differences
    v_diff[:-1, :] = np.abs(img_array[1:, :] - img_array[:-1, :])
    
    # Combine differences
    output = np.maximum(h_diff, v_diff)
    
    return Image.fromarray(normalize_output(output))

def gaussian_kernel(size, sigma):
    """Create a Gaussian kernel"""
    x = np.linspace(-size//2, size//2, size)
    x, y = np.meshgrid(x, x)
    g = np.exp(-(x**2 + y**2)/(2*sigma**2))
    return g / g.sum()

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
    def contrast_op(window):
        return np.abs(window[kernel_size//2, kernel_size//2] - np.mean(window))
    
    output = apply_window_operation(image, kernel_size, contrast_op)
    return Image.fromarray(output)

def variance_operator(image, kernel_size=3):
    """Edge detection based on local variance"""
    def variance_op(window):
        return np.var(window)
    
    output = apply_window_operation(image, kernel_size, variance_op)
    return Image.fromarray(output)

def range_operator(image, kernel_size=3):
    """Edge detection based on local range of intensities"""
    def range_op(window):
        return np.max(window) - np.min(window)
    
    output = apply_window_operation(image, kernel_size, range_op)
    return Image.fromarray(output)
