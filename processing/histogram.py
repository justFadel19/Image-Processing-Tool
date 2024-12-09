from PIL import Image
import matplotlib.pyplot as plt

def calculate_histogram(image):
    """
    Calculate the histogram of a grayscale image.
    
    Args:
        image (PIL.Image.Image): The input grayscale image.
    
    Returns:
        list: Histogram values (frequency of each grayscale value).
    """
    width, height = image.size

    # Initialize a list to count frequencies of each intensity (0-255)
    histogram = [0] * 256

    # Count pixel intensities
    for x in range(width):
        for y in range(height):
            gray = image.getpixel((x, y))
            histogram[gray] += 1

    return histogram

def show_histogram(image):
    """
    Calculate and plot the histogram of a grayscale image.
    
    Args:
        image (PIL.Image.Image): The input grayscale image.
    """
    histogram = calculate_histogram(image)
    
    plt.figure(figsize=(10, 5))
    plt.bar(range(256), histogram, color="gray")
    plt.title("Image Histogram")
    plt.xlabel("Grayscale Value")
    plt.ylabel("Frequency")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

def histogram_equalization(image):
    """
    Perform histogram equalization on a grayscale image.
    
    Args:
        image (PIL.Image.Image): The input grayscale image.
    
    Returns:
        PIL.Image.Image: The histogram-equalized image.
    """
    # Convert the image to grayscale if not already
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size

    # Calculate the histogram
    histogram = calculate_histogram(image)

    # Calculate the cumulative distribution function (CDF)
    cdf = [0] * 256
    cdf[0] = histogram[0]
    for i in range(1, 256):
        cdf[i] = cdf[i - 1] + histogram[i]

    # Normalize the CDF
    cdf_min = min(cdf)
    cdf_max = max(cdf)
    cdf_normalized = [(cdf[i] - cdf_min) * 255 // (cdf_max - cdf_min) for i in range(256)]

    # Create a new image for the equalized result
    equalized_img = Image.new("L", (width, height))

    # Apply the equalized histogram to the image
    for x in range(width):
        for y in range(height):
            gray = image.getpixel((x, y))
            equalized_img.putpixel((x, y), cdf_normalized[gray])

    return equalized_img