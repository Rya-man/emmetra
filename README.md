


# ISP Image Processor

A Python-based standalone application to perform basic Image Signal Processing (ISP) on raw Bayer images. This app implements several ISP routines and allows parameter control for processing.

## Documentation of our Assignments:
https://docs.google.com/document/d/1PnSHAyMdulxG-6h5mR8IXQlvyiZpmqV6MfYaIRAckGo/edit?usp=sharing
## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Processing Pipeline](#processing-pipeline)
- [Combination Outputs](#combination-outputs)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)

## Overview
This ISP application is designed to process 12-bit Bayer raw images and convert them into an 8-bit RGB output image. The app includes features for demosaicing, denoising, gamma correction, and sharpening with a simple GUI built using tkinter.

## Features
- **Demosaic**: Edge-based interpolation to compute missing channels.
- **Gamma Correction**: Adjustable gamma levels using sRGB gamma.
- **Denoise**: Gaussian filter with adjustable sigma.
- **Sharpen**: Unsharp mask filter for edge enhancement.
- **Parameter Control**: Real-time control over processing parameters with sliders.

## Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/virtuoso-04/emmetra.git
    cd emmetra
    ```

2. **Install required libraries**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    python isp_app.py
    ```

## Usage
1. **Load a 12-bit Bayer Raw Image**: Use the "Load Image" button to select your raw image (must be 1920x1280 in GRBG format).
2. **Adjust Parameters**: Use sliders to adjust gamma, sharpening strength, and denoising sigma.
3. **Process Image**: Click "Process Image" to apply processing.
4. **Save Image**: Click "Save Image" to save the processed output.

## Processing Pipeline
The application processes the image through several steps:
1. **Demosaic**
2. **White Balance (Currently inactive)**
3. **Denoise**
4. **Gamma Correction**
5. **Sharpen**

## Combination Outputs
Generate and save images for these combinations as required by the assignment:
- **Demosaic + Gamma**
- **Demosaic + White Balance + Gamma**
- **Demosaic + White Balance + Denoise + Gamma**
- **Demosaic + White Balance + Denoise + Gamma + Sharpen**

## Folder Structure
```plaintext
emmetra/
│
├── processor/
│   ├── demosaic.py
│   ├── denoise.py
│   ├── gamma_correction.py
│   ├── sharpen.py
│   ├── white_balance.py
│   └── __init__.py
│
├── isp_app.py
├── README.md
├── requirements.txt
└── sample_data/ (optional for test images)
