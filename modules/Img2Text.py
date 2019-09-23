# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 17:40:58 2019

@author: Deforest
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image

class Img2Text:
    
    def getText(img_path):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
#    
        cv2.imwrite("D:\Python_project\lineBot\modules\removed_noise.png", img)
        cv2.imwrite(img_path, img)
#    
        result = pytesseract.image_to_string(Image.open(img_path))
        return result
    


if __name__ == "__main__":
    Img2Text.getText("Img2Text.png")
