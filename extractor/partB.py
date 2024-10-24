# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 15:56:51 2023

@author: keert
"""

import cv2
import numpy as np
import os

def remove_tables(img_path):
    #Read the image
    img = cv2.imread(img_path)
    
    #Convert the image to grayscale
    img_path = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #Threshold the image to create a binary image
    _, imgBin = cv2.threshold(img_path, 200, 255, cv2.THRESH_BINARY)
    
    #Invert the binary image
    imgBin[imgBin == 0] = 1
    imgBin[imgBin == 255] = 0

    #Find contours of connected components
    contours, _ = cv2.findContours(imgBin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Remove connected components that are likely to be tables
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h

        #Adjust threshold values based on specific case
        if aspect_ratio > 3 and w > 100:
            img[y:y + h, x:x + w] = 255  #Set the region to white

    return img


def remove_Image(img):
    #Define values for black color 
    black_colour = np.array([0, 0, 0])
    
    #Create a mask for black pixels
    mask_black = cv2.inRange(img, black_colour, black_colour)
    
    #Create a mask for non-black pixels
    mask_white = cv2.bitwise_not(mask_black)
    
    #Set non-black pixels to white
    result_img = cv2.bitwise_and(img, img, mask=mask_white)
    result_img[mask_white != 0] = [255, 255, 255]  # Set the non-black pixels to white
    
    #Convert the result to grayscale
    result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2GRAY)
    
    #Threshold the image to create a binary image
    result_img[result_img < 100] = 1
    result_img[result_img >= 100] = 0
    
    #Erode the binary image
    kernel_d = np.ones((2,2), np.uint8)
    result_img = cv2.erode(result_img, kernel_d, iterations=1)
    
    #Perform morphological closing
    sE = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 80))
    dilate = cv2.morphologyEx(result_img, cv2.MORPH_CLOSE, sE, iterations=1) 
    
    #Find contours of connected components
    contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #Create a mask for the area outside the bounding rectangles
    mask_outside_rects = np.ones_like(dilate, dtype=np.uint8) * 255
    
    #Draw bounding boxes around each contour and update the mask
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        padding = 10
        x -= padding
        y -= padding
        w += 2 * padding
        h += 2 * padding
        
        mask_outside_rects[y:y+h, x:x+w] = 0  #Set the corresponding region in the mask to 0
    
    #Set pixel values outside bounding rectangles to white
    img[mask_outside_rects != 0] = [255, 255, 255]
    
    return img


def extract_sort(img, file_name):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #Make a copy of the image
    img_copy = img.copy()
    
    #Threshold the image to create a binary image
    img[img < 100] = 1
    img[img >= 100] = 0

    #Perform morphological closing
    sE = cv2.getStructuringElement(cv2.MORPH_RECT, (60,60))
    dilate = cv2.morphologyEx(img, cv2.MORPH_CLOSE, sE, iterations=1) 

    #Find contours of connected components
    contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #Create List to store bounding rectangles and contour indices
    rectangles = []

    #Iterate through contours
    for i, contour in enumerate(contours):
        #Get the bounding rectangle for the contour
        x, y, w, h = cv2.boundingRect(contour)
        
        #Add bounding rectangle coordinates and contour index to the list
        rectangles.append({'x': x, 'y': y, 'w': w, 'h': h, 'index': i})
        
    #Sort the list based on x values
    rectangles_sorted = sorted(rectangles, key=lambda r: (r['x']))
   
    #Adjust x values to make them the same if off by 1 to 3 pixels
    for i in range(1, len(rectangles_sorted)):
        prev_x = rectangles_sorted[i - 1]['x']
        current_x = rectangles_sorted[i]['x']

        #Check if the difference is within the desired range (1 to 3 pixels)
        if 1 <= current_x - prev_x <= 3:
            rectangles_sorted[i]['x'] = prev_x
       
    #Sort the list based on y values
    rectangles_sorted = sorted(rectangles_sorted, key=lambda r: (r['x'], r['y']))

    #Iterate through sorted rectangles
    for i, rect in enumerate(rectangles_sorted):
        # Get the bounding rectangle coordinates
        x, y, w, h = rect['x'], rect['y'], rect['w'], rect['h']
         
        #Crop the region inside the bounding box
        text_region = img_copy[y:y+h, x:x+w]
        
        #Add margins around the text region
        margin = 10 #Set accordingly
        paragraphs = cv2.copyMakeBorder(text_region, margin, margin, margin, margin, cv2.BORDER_CONSTANT, value=255)

        #Create a folder for each image if it doesn't exist
        output_folder = f'{file_name}'
        os.makedirs(output_folder, exist_ok=True)

        #Save the extracted contour as an image within the respective folder
        cv2.imwrite(f'{output_folder}/Paragraph_{i + 1}.png', paragraphs)
     


img_paths = ['input_images/001.png', 'input_images/002.png', 'input_images/003.png', 'input_images/004.png', 
             'input_images/005.png', 'input_images/006.png', 'input_images/007.png', 'input_images/008.png']

for img_path in img_paths:
    #Extract the file name without the extension and folder name
    file_name = os.path.splitext(os.path.basename(img_path))[0]
    original_image = cv2.imread(img_path)

    no_table = remove_tables(img_path)
    no_image = remove_Image(no_table)
    extract_sort(no_image, file_name)
    

'''
#Run code for 1 image at once
#img_path = 'input_images/001.png'
#img_path = 'input_images/002.png'
#img_path = 'input_images/003.png'
#img_path = 'input_images/004.png'
#img_path = 'input_images/005.png'
#img_path = 'input_images/006.png'
#img_path = 'input_images/007.png'
#img_path = 'input_images/008.png'

file_name = os.path.splitext(os.path.basename(img_path))[0]

no_table = remove_tables(img_path)
no_image = remove_Image(no_table)
extract_sort(no_image, file_name)
'''
