# Leif Ekstrom
# ENGN2045
# Final Project
# Due: 4/20/2021

from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv
import pytesseract
# Put where tesseract.exe is located on your own computer
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import web_scraper
    
    
def main():
    # Filepath of the desired image
    filePath = 'textChestnut.jpg'
    
    textList = []
    im = cv.imread(filePath)
    
    # Identify and extract text from the image
    text = pytesseract.image_to_string(im)
    # Remove superfluous marker character that tesseract adds at the end of the string
    parsedText = text[:-1].replace('\n','')
    # Using a list here so that support for images containing multiple words can be implemented in the future
    textList.append(parsedText)
    
    # Draw boxes around each character in the image
    h, w, c = im.shape
    boxes = pytesseract.image_to_boxes(im) 
    for b in boxes.splitlines():
        b = b.split(' ')
        imTess = cv.rectangle(im, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
    
    # Use the webscraper to find the translation for the word found by the computer vision section
    web_scraper.get_translation(parsedText)
    
    # Display the image with boxes - 'tesseracted' image
    fig, ax = plt.subplots(1, 1)
    plt.tight_layout()
    ax.imshow(imTess,cmap='gray')
    ax.set_title(parsedText)
    
    plt.show()
    

if __name__=="__main__": 
    main()