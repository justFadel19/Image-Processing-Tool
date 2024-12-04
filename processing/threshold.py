import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def calculate_threshold(image):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Calculate average pixel value as threshold
    threshold = np.mean(img_array)
    
    # Create a figure to display the threshold information
    plt.figure(figsize=(10, 4))
    
    # Plot histogram
    plt.subplot(121)
    plt.hist(img_array.ravel(), bins=256, range=(0, 256), density=True, color='gray', alpha=0.7)
    plt.axvline(x=threshold, color='r', linestyle='--', label=f'Threshold = {threshold:.1f}')
    plt.title('Image Histogram with Threshold')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.legend()
    
    # Plot threshold line on image
    plt.subplot(122)
    plt.imshow(img_array, cmap='gray')
    plt.title(f'Original Image\nOptimal Threshold = {threshold:.1f}')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()
    
    # Return the original image and the calculated threshold
    return image