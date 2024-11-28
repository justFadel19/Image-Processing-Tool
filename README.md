# Image Processing Tool

## Overview
This project is a Python-based Image Processing Tool featuring a Graphical User Interface (GUI). It implements fundamental and advanced image processing operations from scratch, without relying on library functions for complete solutions.

The tool is designed for educational purposes, providing insights into the underlying processes of image manipulation and analysis.

---

## Features

### Core Functionalities
- **Image Uploading**: Load images from your device into the tool.
- **Dynamic Visualization**: Display processed images alongside the original image.
- **Image Processing Operations**:
  - **Color Conversion**:
    - Convert image to grayscale.
  - **Thresholding**:
    - Calculate image threshold using pixel averages.
    - Apply simple and advanced halftoning (error diffusion).
  - **Histogram Processing**:
    - Generate histograms of images.
    - Perform histogram equalization.
  - **Edge Detection**:
    - Simple methods: Sobel, Prewitt, Kirsch compass masks.
    - Advanced methods: Homogeneity, difference operator, difference of Gaussians, contrast-based, variance, and range detection.
  - **Filtering**:
    - High-pass and low-pass filters.
    - Median filtering.
  - **Image Operations**:
    - Add and subtract image copies.
    - Invert images.
  - **Segmentation**:
    - Manual and histogram-based techniques (peak, valley, adaptive).

---

## Installation

### Prerequisites
- **Python**: Version 3.8+
- **Required libraries**:
  - `tkinter` (for GUI)
  - `numpy`
  - `Pillow`
  - `matplotlib`

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/Image-Processing-Tool.git
   cd Image-Processing-Tool
   ```
2. Install dependencies:
   ```bash
    pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
    python app.py
   ```
## Usage
1. **Launch the tool**.
2. **Upload an image** using the **Upload Image** button.
3. Select any **processing operation** by clicking the corresponding button.
4. View the **processed image** and corresponding results in real time.

## Project Structure
```bash
Image-Processing-Tool/
│
├── app.py                 
├── processing/
│   ├── color.py            
│   ├── threshold.py
│   ├── halftone.py       
│   ├── histogram.py        
│   ├── simple_edge_detection.py
│   ├── advanced_edge_detection.py
│   ├── filtering.py
│   ├── image_operations.py       
│   ├── segmentation.py     
│   └── utils.py            
│
├── assets/                 
├── README.md               
└── requirements.txt       
```
## Implementation Details

### Custom Implementation
Each operation is written from scratch using basic operations like sum, min, max, and median. For example:

- **Grayscale Conversion**:
   ```python
   def to_grayscale(image):
       return image.convert('L')
   ```
---

## Graphical User Interface
- Developed using **Tkinter**.
- Organized into intuitive sections:
  - **Upload and display**.
  - **Operations grouped by categories** (color, histogram, edge detection, etc.).

---

## Contribution
We welcome contributions! Follow these steps:

1. **Fork the repository**.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
    git commit -m "Add your feature"
   ```
4. Push your branch:
   ```bash
    git push origin feature/your-feature
   ```
5. **Submit a pull request**.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.


