import cv2
import numpy as np

def adraw(img, a, func, *args, **kwargs):
    return cv2.addWeighted(img, 1.0-a, func(img.copy(), *args, **kwargs), a, 0, img)