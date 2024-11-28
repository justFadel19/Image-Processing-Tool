import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def apply_histogram(image):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Get image data as numpy array
    img_array = np.array(image)
    
    # Calculate histogram
    histogram = np.histogram(img_array, bins=256, range=(0, 256))[0]
    
    # Create a new figure
    plt.figure(figsize=(8, 6))
    plt.title('Image Histogram')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    
    # Plot histogram
    plt.plot(histogram)
    plt.grid(True)
    
    # Show the plot
    plt.show()
    
    return image

def apply_histogram_equalization(image):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Convert image to numpy array
    img_array = np.array(image)
    
    # Calculate histogram
    histogram = np.histogram(img_array, bins=256, range=(0, 256))[0]
    
    # Calculate cumulative distribution function (CDF)
    cdf = histogram.cumsum()
    
    # Normalize CDF
    cdf_normalized = cdf * float(histogram.max()) / cdf.max()
    
    # Create lookup table
    lookup_table = np.interp(range(256), range(256), cdf_normalized)
    
    # Apply lookup table to image
    equalized_array = lookup_table[img_array]
    
    # Convert back to PIL Image
    equalized_image = Image.fromarray(np.uint8(equalized_array))
    
    return equalized_image
