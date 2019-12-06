import os
import sys
import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm



def rgb_to_grayscale(image):
    """
    Converts RGB image to the grayscale format

    Parameters
    ----------
    image : array, shape (H, W, 3)
        image of size H x W

    Returns
    -------
    image : array, shape(H, W)
        grayscaled image
    """
    if len(image.shape) == 2: # already grayscaled
        return image
    return np.dot(image, [0.299, 0.587, 0.114])
    
    
def get_ASCII_represantation(image, height, width):
    """
    Converts image to the ASCII format

    Parameters
    ----------
    image : PIL.Image

    height : int
        height of ASCII image
        
    width : int
        width of ASCII image

    Returns
    -------
    ascii_image : str, length(height * (width + 1))
        rows of ASCII image separated by line ending symbol
    """
    image = image.resize((width, height))
    image = rgb_to_grayscale(np.array(image)).astype(np.uint8)
    characters = ['@', 'B', 'M', 'r', 'i', ':', '.', ' ']
    image //= (256 // len(characters)) # getting ids of characters for each pixel
    ascii_image = ''
    for row in image:
        for pixel in row:
            ascii_image += characters[pixel]
        ascii_image += '\n'
    return ascii_image
    

def process_image(filename, height, width, to_save_filename):
    """
    Converts image to the ASCII format and saves it to the file

    Parameters
    ----------
    filename : str
        file name of the image to be converted

    height : int
        height of ASCII image
        
    width : int
        width of ASCII image

    to_save_filename : str
        file name where the result image should be written
    """
    file = open(to_save_filename, 'w')
    image = Image.open(filename)
    ascii_image = get_ASCII_represantation(image, height, width)
    print(height, width, file=file)
    print(ascii_image, file=file)
    file.close()
    
    
def process_video(filename, height, width, to_save_filename):
    """
    Converts video to the ASCII format and saves it to the file

    Parameters
    ----------
    filename : str
        file name of the video to be converted

    height : int
        height of ASCII video
        
    width : int
        width of ASCII video

    to_save_filename : str
        file name where the result video should be written
    """
    reader = cv2.VideoCapture(filename)
    progress_bar = tqdm()
    file = open(to_save_filename, 'w')
    print(height, width, file=file)
    while True:
        read, frame = reader.read()
        if not read:
            break
        frame = Image.fromarray(frame)
        print(get_ASCII_represantation(frame, height, width), file=file)
        progress_bar.update()
    file.close()
    

def wrong_parameters_notification():
    print('''Please, provide 5 parameters: 
  1) type_process - 'video' or 'image'
  2) input_file - path to the input video/image
  3) height - height of the result ASCII-video/image file
  4) width - width of the result ASCII-video/image file
  5) output_file - path to the output ASCII-video/image file''')
    exit()
    
    
if len(sys.argv) != 6:
    wrong_parameters_notification()
type_process, input_file, height, width, output_file = sys.argv[1:]
if type_process not in ['video', 'image']:
    print('Parameter type_process should be \'video\' or \'image\'')
    exit()
if not os.path.exists(input_file):
    print('File \'{}\' doesn\'t exists'.format(input_file))
    exit()
try:
    height = int(height)
    width = int(width)
    assert(1 <= height <= 2000 and 1 <= width <= 2000)
except Exception as e:
    print('Height and width parameters should be integers from 1 to 2000')
    exit()
if type_process == 'image':
    process_image(input_file, height, width, output_file)
else:
    process_video(input_file, height, width, output_file)