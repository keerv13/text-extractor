# Document Image Preprocessing and Region Extraction
This project processes scanned document images to remove tables and embedded images, then extracts and sorts paragraph regions. The project is designed to handle papers with single, double, or triple-column formats.

## Dependencies
* Python 3.x
* OpenCV (cv2)
* NumPy (numpy)


## How to Run
1. Clone the repo
```
git clone https://github.com/keerv13/text-extractor.git
```
2. Make sure you have Python 3.x installed. Then install the required packages:
```pip install opencv-python numpy```
3. Prepare Input Images
* Place your document images in a folder named input_images/ or use existing doucments in input_images/.
* Supported formats include .png, .jpg, .jpeg.
4. Run the Script
* Process All Images
```python main.py```
* Process a Single Image
** Inside main.py, comment/uncomment the image path you want then run:
```python main.py```

## key Features
* Remove tables
* Remove images
* Extract & Sort Paragraphs

## Example Input/Output
<img width="1334" height="679" alt="Image" src="https://github.com/user-attachments/assets/98ff6ab5-bc9b-4c26-8de7-1f8dd568a9d4" />
