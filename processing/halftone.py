from PIL import Image
import numpy as np

def apply_halftone(image, sample_size=2):
    # Convert to grayscale
    grayscale = image.convert("L")
    width, height = grayscale.size
    
    # Create output image with doubled dimensions for dots
    out_width = width * 2
    out_height = height * 2
    output_image = Image.new('L', (out_width, out_height), 255)
    
    # Get pixel data
    pixels = np.array(grayscale)
    
    # Process each block
    for y in range(0, height, sample_size):
        for x in range(0, width, sample_size):
            # Get the average value of the block
            block = pixels[y:min(y+sample_size, height), x:min(x+sample_size, width)]
            avg = np.mean(block)
            
            # Calculate dot size (0-255 -> 0-sample_size)
            dot_size = int((255 - avg) * sample_size / 255)
            
            if dot_size > 0:
                # Draw black dot
                for dy in range(dot_size):
                    for dx in range(dot_size):
                        out_x = (x * 2) + dx
                        out_y = (y * 2) + dy
                        if out_x < out_width and out_y < out_height:
                            output_image.putpixel((out_x, out_y), 0)
    
    return output_image
