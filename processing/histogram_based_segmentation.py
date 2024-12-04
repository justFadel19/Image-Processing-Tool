import numpy as np
from PIL import Image
from .histogram import get_histogram

def manual_segmentation(image, threshold):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    segmented = np.where(np.array(image) > threshold, 255, 0).astype(np.uint8)
    return Image.fromarray(segmented)

def peak_segmentation(image):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Find peaks (local maxima)
    peaks = []
    for i in range(1, 255):
        if histogram[i-1] < histogram[i] > histogram[i+1]:
            peaks.append(i)
    
    if len(peaks) < 2:
        # If less than 2 peaks, use mean as threshold
        threshold = np.mean(np.array(image))
    else:
        # Use valley between two highest peaks
        peaks.sort(key=lambda x: histogram[x], reverse=True)
        peak1, peak2 = sorted(peaks[:2])
        threshold = (peak1 + peak2) // 2
    
    return manual_segmentation(image, threshold)

def valley_segmentation(image):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Find valleys (local minima)
    valleys = []
    for i in range(1, 255):
        if histogram[i-1] > histogram[i] < histogram[i+1]:
            valleys.append(i)
    
    if not valleys:
        # If no valleys found, use mean as threshold
        threshold = np.mean(np.array(image))
    else:
        # Use the deepest valley
        threshold = min(valleys, key=lambda x: histogram[x])
    
    return manual_segmentation(image, threshold)

def adaptive_segmentation(image, block_size=16):
    # Convert image to grayscale if it isn't already
    if image.mode != 'L':
        image = image.convert('L')
    
    img_array = np.array(image)
    height, width = img_array.shape
    
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            # Get block
            block = img_array[i:min(i+block_size, height), 
                            j:min(j+block_size, width)]
            
            # Calculate local threshold
            threshold = np.mean(block)
            
            # Apply threshold to block
            result[i:min(i+block_size, height), 
                  j:min(j+block_size, width)] = np.where(block > threshold, 255, 0)
    
    return Image.fromarray(result)
