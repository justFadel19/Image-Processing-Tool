from PIL import Image

def simple_halftone(image):
    """
    Apply a simple halftone effect using threshold-based binarization.
    
    Args:
        image (PIL.Image.Image): The input grayscale image.

    Returns:
        PIL.Image.Image: The halftone image.
    """
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size

    # Calculate a threshold based on the average intensity
    pixel_values = [image.getpixel((x, y)) for x in range(width) for y in range(height)]
    threshold = sum(pixel_values) // len(pixel_values)
    print(f"Threshold for halftone: {threshold}")

    # Create a new image for the halftone result
    halftone_img = Image.new("1", (width, height))  # '1' mode for binary images

    # Apply threshold-based halftoning
    for x in range(width):
        for y in range(height):
            gray = image.getpixel((x, y))
            value = 255 if gray > threshold else 0
            halftone_img.putpixel((x, y), value)

    return halftone_img


def error_diffusion_halftoning(image, threshold=128):
    """
    Apply an advanced halftone effect using Floyd-Steinberg error diffusion.
    
    Args:
        image (PIL.Image.Image): The input grayscale image.
        threshold (int): The threshold value for binarization.

    Returns:
        PIL.Image.Image: The halftone image.
    """
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')

    width, height = image.size

    # Convert image to a list of lists for manipulation
    img_array = [[image.getpixel((x, y)) for x in range(width)] for y in range(height)]

    # Create a binary array for the halftone result
    halftone_array = [[0 for _ in range(width)] for _ in range(height)]

    # Floyd-Steinberg error diffusion kernel
    diffusion_kernel = [(1, 0, 7 / 16), (-1, 1, 3 / 16), (0, 1, 5 / 16), (1, 1, 1 / 16)]

    # Apply error diffusion
    for y in range(height):
        for x in range(width):
            old_pixel = img_array[y][x]
            new_pixel = 255 if old_pixel >= threshold else 0
            halftone_array[y][x] = new_pixel
            error = old_pixel - new_pixel

            # Spread the error to neighboring pixels
            for dx, dy, weight in diffusion_kernel:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    img_array[ny][nx] += error * weight

    # Create a new image for the halftone result
    halftone_img = Image.new("1", (width, height))
    for y in range(height):
        for x in range(width):
            halftone_img.putpixel((x, y), halftone_array[y][x])

    return halftone_img