import numpy as np
from PIL import Image

def apply_sobel(image):
    """
    Apply Sobel edge detection to an image.
    
    The Sobel operator is used in image processing and computer vision, particularly within edge detection algorithms
    where it creates an image emphasizing edges. It uses two 3x3 kernels (sobel_x and sobel_y) to calculate the 
    gradient in the x and y directions. The magnitude of the gradient is then computed to highlight the edges.

    Args:
        image (PIL.Image.Image): The input image to be processed.

    Returns:
        PIL.Image.Image: The image with Sobel edge detection applied.
    """
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')

    width, height = image.size
    image_array = np.array(image, dtype=np.float64)

    # Sobel operators
    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    # Initialize gradient arrays
    gradient_x = np.zeros((height, width), dtype=np.float64)
    gradient_y = np.zeros((height, width), dtype=np.float64)

    # Apply convolution manually
    for i in range(1, height-1):
        for j in range(1, width-1):
            gx = 0
            gy = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    gx += image_array[i+k, j+l] * sobel_x[k+1][l+1]
                    gy += image_array[i+k, j+l] * sobel_y[k+1][l+1]
            gradient_x[i, j] = gx
            gradient_y[i, j] = gy

    # Calculate magnitude
    magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)

    return Image.fromarray(magnitude)


def apply_prewitt(image):
    """
    Apply Prewitt edge detection to an image.
    
    The Prewitt operator is used in image processing and computer vision, particularly within edge detection algorithms
    where it creates an image emphasizing edges. It uses two 3x3 kernels (prewitt_x and prewitt_y) to calculate the 
    gradient in the x and y directions. The magnitude of the gradient is then computed to highlight the edges.

    Args:
        image (PIL.Image.Image): The input image to be processed.

    Returns:
        PIL.Image.Image: The image with Prewitt edge detection applied.
    """
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')

    width, height = image.size
    image_array = np.array(image, dtype=np.float64)

    # Prewitt operators
    prewitt_x = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    prewitt_y = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]

    # Initialize gradient arrays
    gradient_x = np.zeros((height, width), dtype=np.float64)
    gradient_y = np.zeros((height, width), dtype=np.float64)

    # Apply convolution manually
    for i in range(1, height-1):
        for j in range(1, width-1):
            gx = 0
            gy = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    gx += image_array[i+k, j+l] * prewitt_x[k+1][l+1]
                    gy += image_array[i+k, j+l] * prewitt_y[k+1][l+1]
            gradient_x[i, j] = gx
            gradient_y[i, j] = gy

    # Calculate magnitude
    magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)

    return Image.fromarray(magnitude)

def apply_kirsch(image):
    """
    Apply Kirsch edge detection to an image.
    
    The Kirsch operator is used in image processing and computer vision, particularly within edge detection algorithms
    where it creates an image emphasizing edges. It uses eight 3x3 kernels to calculate the gradient in eight different
    directions. The maximum response from these directions is then computed to highlight the edges.

    Args:
        image (PIL.Image.Image): The input image to be processed.

    Returns:
        PIL.Image.Image: The image with Kirsch edge detection applied.
    """
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')

    width, height = image.size
    image_array = np.array(image, dtype=np.float64)

    # Kirsch operators (8 directions)
    kirsch_filters = [
        [[ 5,  5,  5], [-3,  0, -3], [-3, -3, -3]],  # North
        [[ 5,  5, -3], [ 5,  0, -3], [-3, -3, -3]],  # North East
        [[ 5, -3, -3], [ 5,  0, -3], [ 5, -3, -3]],  # East
        [[-3, -3, -3], [ 5,  0, -3], [ 5,  5, -3]],  # South East
        [[-3, -3, -3], [-3,  0, -3], [ 5,  5,  5]],  # South
        [[-3, -3, -3], [-3,  0,  5], [-3,  5,  5]],  # South West
        [[-3, -3,  5], [-3,  0,  5], [-3, -3,  5]],  # West
        [[-3,  5,  5], [-3,  0,  5], [-3, -3, -3]]   # North West
    ]

    # Initialize maximum magnitude array
    max_magnitude = np.zeros((height, width), dtype=np.float64)

    # Apply all directions and get maximum response
    for kernel in kirsch_filters:
        response = np.zeros((height, width), dtype=np.float64)
        for i in range(1, height-1):
            for j in range(1, width-1):
                value = 0
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        value += image_array[i+k, j+l] * kernel[k+1][l+1]
                response[i, j] = value
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