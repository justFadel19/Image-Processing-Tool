import numpy as np
from PIL import Image

def calculate_histogram(image):
    """
    Calculate the histogram of a grayscale image.
    
    Args:
        image (PIL.Image.Image): The input grayscale image.
    
    Returns:
        list: Histogram values (frequency of each grayscale value).
    """
    width, height = image.size
    histogram = [0] * 256

    for x in range(width):
        for y in range(height):
            gray = image.getpixel((x, y))
            histogram[gray] += 1

    return histogram

def manual_segmentation(image, threshold):
    """
    Segment the image using a manual threshold.
    
    Args:
        image (PIL.Image.Image): The input grayscale image.
        threshold (int): The threshold value for segmentation.
    
    Returns:
        PIL.Image.Image: The segmented image.
    """
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size
    img_array = np.array(image, dtype=np.uint8)
    segmented = np.zeros_like(img_array)

    for x in range(width):
        for y in range(height):
            if img_array[y, x] > threshold:
                segmented[y, x] = 255
            else:
                segmented[y, x] = 0

    return Image.fromarray(segmented)

def peak_segmentation(image):
    """
    Segment the image using peak detection.
    
    Args:
        image (PIL.Image.Image): The input grayscale image.
    
    Returns:
        PIL.Image.Image: The segmented image.
    """
    if image.mode != 'L':
        image = image.convert('L')
    
    histogram = calculate_histogram(image)
    peaks = []

    for i in range(1, 255):
        if histogram[i-1] < histogram[i] > histogram[i+1]:
            peaks.append(i)
    
    if len(peaks) < 2:
        threshold = sum(sum(image.getpixel((x, y)) for x in range(image.width)) for y in range(image.height)) // (image.width * image.height)
    else:
        peaks.sort(key=lambda x: histogram[x], reverse=True)
        peak1, peak2 = sorted(peaks[:2])
        threshold = (peak1 + peak2) // 2
    
    return manual_segmentation(image, threshold)

def valley_segmentation(image):
    """
    Segment the image using valley detection.
    
    Args:
        image (PIL.Image.Image): The input grayscale image.
    
    Returns:
        PIL.Image.Image: The segmented image.
    """
    if image.mode != 'L':
        image = image.convert('L')
    
    histogram = calculate_histogram(image)
    valleys = []

    for i in range(1, 255):
        if histogram[i-1] > histogram[i] < histogram[i+1]:
            valleys.append(i)
    
    if not valleys:
        threshold = sum(sum(image.getpixel((x, y)) for x in range(image.width)) for y in range(image.height)) // (image.width * image.height)
    else:
        threshold = min(valleys, key=lambda x: histogram[x])
    
    return manual_segmentation(image, threshold)

def adaptive_segmentation(image, block_size=16):
    """
    Segment the image using adaptive thresholding.
    
    Args:
        image (PIL.Image.Image): The input grayscale image.
        block_size (int): The size of the blocks for local thresholding.
    
    Returns:
        PIL.Image.Image: The segmented image.
    """
    if image.mode != 'L':
        image = image.convert('L')
    
    width, height = image.size
    img_array = np.array(image, dtype=np.uint8)
    result = np.zeros_like(img_array)

    # Ensure block_size is not larger than image dimensions
    block_size = min(block_size, width, height)

    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            # Calculate block boundaries
            block_end_i = min(i + block_size, height)
            block_end_j = min(j + block_size, width)
            
            # Extract current block
            block = img_array[i:block_end_i, j:block_end_j]
            
            # Calculate mean threshold for the block
            threshold = np.mean(block)
            
            # Apply thresholding to the block
            mask = block > threshold
            result[i:block_end_i, j:block_end_j][mask] = 255
            result[i:block_end_i, j:block_end_j][~mask] = 0
    
    return Image.fromarray(result)