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

def apply_sobel(image):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')

    image_array = np.array(image, dtype=np.float64)

    # Sobel operators
    sobel_x = np.array([[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]])
    
    sobel_y = np.array([[-1, -2, -1],
                       [0, 0, 0],
                       [1, 2, 1]])
    
    # Apply convolution
    gradient_x = convolve(image_array, sobel_x)
    gradient_y = convolve(image_array, sobel_y)
    
    # Calculate magnitude
    magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
    
    return Image.fromarray(magnitude)

def apply_prewitt(image):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    image_array = np.array(image, dtype=np.float64)
    
    # Prewitt operators
    prewitt_x = np.array([[-1, 0, 1],
                         [-1, 0, 1],
                         [-1, 0, 1]])
    
    prewitt_y = np.array([[-1, -1, -1],
                         [0, 0, 0],
                         [1, 1, 1]])
    
    # Apply convolution
    gradient_x = convolve(image_array, prewitt_x)
    gradient_y = convolve(image_array, prewitt_y)
    
    # Calculate magnitude
    magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
    
    return Image.fromarray(magnitude)

def apply_kirsch(image):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    image_array = np.array(image, dtype=np.float64)
    
    # Kirsch operators (8 directions)
    kirsch_filters = [
        np.array([[ 5,  5,  5],
                 [-3,  0, -3],
                 [-3, -3, -3]]),  # North
        np.array([[ 5,  5, -3],
                 [ 5,  0, -3],
                 [-3, -3, -3]]),  # North East
        np.array([[ 5, -3, -3],
                 [ 5,  0, -3],
                 [ 5, -3, -3]]),  # East
        np.array([[-3, -3, -3],
                 [ 5,  0, -3],
                 [ 5,  5, -3]]),  # South East
        np.array([[-3, -3, -3],
                 [-3,  0, -3],
                 [ 5,  5,  5]]),  # South
        np.array([[-3, -3, -3],
                 [-3,  0,  5],
                 [-3,  5,  5]]),  # South West
        np.array([[-3, -3,  5],
                 [-3,  0,  5],
                 [-3, -3,  5]]),  # West
        np.array([[-3,  5,  5],
                 [-3,  0,  5],
                 [-3, -3, -3]])   # North West
    ]
    
    # Apply all directions and get maximum response
    max_magnitude = np.zeros_like(image_array, dtype=float)
    
    for kernel in kirsch_filters:
        response = convolve(image_array, kernel)
        max_magnitude = np.maximum(max_magnitude, response)
    
    # Normalize magnitude
    magnitude = np.clip(max_magnitude, 0, 255).astype(np.uint8)
    
    return Image.fromarray(magnitude)

def edge_detection(image, method="sobel"):
    """
    Apply edge detection to an image using the specified method.
    
    Args:
        image: PIL Image object
        method: string, one of "sobel", "prewitt", or "kirsch"
    
    Returns:
        PIL Image object with detected edges
    """
    if method == "sobel":
        return apply_sobel(image)
    elif method == "prewitt":
        return apply_prewitt(image)
    elif method == "kirsch":
        return apply_kirsch(image)
    else:
        return apply_sobel(image)  # default to sobel