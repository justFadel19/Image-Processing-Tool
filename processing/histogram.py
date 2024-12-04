import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def show_histogram(image):
    # Convert image to grayscale if it isn't already
    if image.mode != "L":
        image = image.convert("L")

    # Get image data as numpy array
    img_array = np.array(image)

    flat = img_array.flatten()  # Flatten the image to 1D for histogram computation
    
    # Compute the histogram
    hist, bins = np.histogram(flat, bins=256, range=[0, 256], density=False)

    # Create a new figure
    plt.figure(figsize=(8, 6))
    plt.bar(range(256), hist, color='gray', alpha=0.7)
    plt.title("Image Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.grid(True, alpha=0.3)

    # Show the plot
    plt.show()

    return image


def histogram_equalization(image):
    # Convert the image to grayscale if not already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Get image data as numpy array
    img_array = np.array(image)
    
    flat = img_array.flatten()  # Flatten the image to 1D for histogram computation
    
    # Compute the histogram
    hist, bins = np.histogram(flat, bins=256, range=[0, 256], density=True)
    
    # Compute the CDF (Cumulative Distribution Function)
    cdf = hist.cumsum()  # Cumulative sum of histogram values
    cdf_normalized = cdf * (255 / cdf[-1])  # Normalize to range [0, 255]
    
    # Apply the equalization transformation
    equalized_img_array = np.interp(flat, bins[:-1], cdf_normalized).reshape(img_array.shape)
    
    # Convert back to an image
    return Image.fromarray(equalized_img_array.astype(np.uint8))
