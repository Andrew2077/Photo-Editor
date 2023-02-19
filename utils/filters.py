import cv2
import PIL
import numpy as np
from PIL import Image, ImageEnhance



def gray_scale_filer(image:PIL.Image.Image, convert_to_RGB: bool = True):
    if convert_to_RGB:
        image = np.array(image.convert("RGB"))
    gray_scale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return  gray_scale

def black_white_filter(image:PIL.Image.Image, intensity: int):
    gray_scaled_img = gray_scale_filer(image)
    (_, black_white_image) = cv2.threshold(gray_scaled_img, intensity, 255, cv2.THRESH_BINARY)
    return black_white_image

def sktech_filter(image: PIL.Image.Image, intensity: int):
        gray_scale_image = gray_scale_filer(image)
        inv_gray_scale = 255 - gray_scale_image
        blur_image = cv2.GaussianBlur(inv_gray_scale, (intensity, intensity), 0, 0)
        sketch = cv2.divide(gray_scale_image, 255 - blur_image, scale=256)
        return sketch

def blur_filter(image: PIL.Image.Image, intensity: int):
    edited_image = cv2.GaussianBlur(image, (intensity, intensity), 0, 0)
    edited_image = cv2.cvtColor(edited_image, cv2.COLOR_BGR2RGB)
    return edited_image