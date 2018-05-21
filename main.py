#!/usr/bin/python3

from PIL import Image
import pyscreenshot as ImageGrab
import pytesseract
import cv2
import os

preprocess = "thresh"

def screenshot():
    im=ImageGrab.grab()
    path="Screenshots/screenshot.png"
    im.save(path)
    return path

def crop(image_path, saved_location):
    img = Image.open(image_path)
    w, h = img.size
    img = img.crop((1280, 400, w, h-400))
    img.save(saved_location)
    

def ocr(imageplace, preprocess):
    #load example and convert to grayscale
    image = cv2.imread(imageplace)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # check to see if we should apply thresholding to preprocess the
    # image
    if preprocess == "thresh":
	    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # make a check to see if median blurring should be done to remove
    # noise
    elif preprocess == "blur":
    	    gray = cv2.medianBlur(gray, 3)

    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    return text

if __name__ == "__main__":
    cropsave = 'Screenshots/cropped.png'
    crop(screenshot(), cropsave)
    print(ocr(cropsave, 'blur'))

