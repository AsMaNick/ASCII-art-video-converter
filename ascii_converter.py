from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
from PIL import Image
import cv2
import time
import os
import sys


filter = np.array([[-1, -1, -1],
                   [-1, 8, -1],
                   [-1, -1, -1]])


def rgb_to_gray(img):
    if len(img.shape) == 2:
        return img
    return np.dot(img, [0.299, 0.587, 0.114])
    
    
def get_symbol(pixel):
    #return [' ', '#'][abs(pixel) > 30]
    #return [' ', '.', '$', '%', '-', '&', '*', '+'][min(7, abs(pixel) // 16)]
    return [' ', '.', ':', 'i', 'r', 'M', 'B', '@'][pixel // 32]
    try:
        return '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^` '[(255 - pixel) * 67 // 255]
    except:
        print((255 - pixel) * 69 // 255)
        exit((255 - pixel) * 69 // 255)
    
    
def get_str(img, h, w):
    img = img.resize((w, h))  # resizes image in-place
    img = rgb_to_gray(np.array(img)).astype(np.uint8) // 32
    s = ''
    for row in img:
        for pixel in row:
            #s += [' ', '.', ':', 'i', 'r', 'M', 'B', '@'][pixel]
            s += ['@', 'B', 'M', 'r', 'i', ':', '.', ' '][pixel]
        s += '\n'
    return s
    

def process_video(filename, h, w):
    cam = cv2.VideoCapture(filename)
    tq = tqdm()
    f = open('res.txt', 'w')
    print(h, w, file=f)
    while True:
        ok, frame = cam.read()
        if not ok:
            break
        frame = Image.fromarray(frame)
        print(get_str(frame, h, w), file=f)
        tq.update()        
        
        
def process_image(img, h, w, file):
    str = get_str(img, h, w)
    print(h, w, file=file)
    print(str, file=file)
    file.close()
    
    
#process_image(Image.open('videos/dimitrov.png'), 178, 600, file=open('res600_my.txt', 'w'))
#process_video('videos/vals.mp4', 178, 600)
#process_video('videos/dolgopolov.mp4', 178, 600)