import numpy as np
from PIL import Image

def edge_detection(image, method="sobel"):
    # Convert image to grayscale if it isn't already
    grayscale = image.convert("L")
    image_array = np.array(grayscale, dtype=np.float64)  # Use float64 for better precision
    result_array = None

    if method == "sobel":
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        gx = convolve(image_array, sobel_x)
        gy = convolve(image_array, sobel_y)
        result_array = np.sqrt(gx ** 2 + gy ** 2)
    
    elif method == "prewitt":
        prewitt_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        prewitt_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
        gx = convolve(image_array, prewitt_x)
        gy = convolve(image_array, prewitt_y)
        result_array = np.sqrt(gx ** 2 + gy ** 2)
    
    elif method == "kirsch":
        # Kirsch operators (8 directions)
        kirsch_kernels = [
            np.array([[ 5,  5,  5],
                     [-3,  0, -3],
                     [-3, -3, -3]]),  # North
            np.array([[ 5,  5, -3],
                     [ 5,  0, -3],
                     [-3, -3, -3]]),  # North-East
            np.array([[ 5, -3, -3],
                     [ 5,  0, -3],
                     [ 5, -3, -3]]),  # East
            np.array([[-3, -3, -3],
                     [ 5,  0, -3],
                     [ 5,  5, -3]]),  # South-East
            np.array([[-3, -3, -3],
                     [-3,  0, -3],
                     [ 5,  5,  5]]),  # South
            np.array([[-3, -3, -3],
                     [-3,  0,  5],
                     [-3,  5,  5]]),  # South-West
            np.array([[-3, -3,  5],
                     [-3,  0,  5],
                     [-3, -3,  5]]),  # West
            np.array([[-3,  5,  5],
                     [-3,  0,  5],
                     [-3, -3, -3]])   # North-West
        ]
        
        # Apply all 8 kernels and get maximum response
        responses = []
        for kernel in kirsch_kernels:
            responses.append(np.abs(convolve(image_array, kernel)))
        result_array = np.maximum.reduce(responses)

    # Normalize result to 0-255 range
    if result_array is not None:
        # Enhance contrast by adjusting the normalization
        p2, p98 = np.percentile(result_array, (2, 98))
        result_array = np.clip(result_array, p2, p98)
        result_array = (result_array - p2) * (255.0 / (p98 - p2))
        result_array = np.clip(result_array, 0, 255)
        return Image.fromarray(np.uint8(result_array))
    else:
        return image

def convolve(image_array, kernel):
    kernel_height, kernel_width = kernel.shape
    image_height, image_width = image_array.shape
    output = np.zeros_like(image_array)

    # Use reflect padding instead of constant padding for better edge handling
    padded_image = np.pad(image_array, ((kernel_height // 2, kernel_height // 2),
                                       (kernel_width // 2, kernel_width // 2)), 
                         mode="reflect")

    for i in range(image_height):
        for j in range(image_width):
            region = padded_image[i:i + kernel_height, j:j + kernel_width]
            output[i, j] = np.sum(region * kernel)

    return output
