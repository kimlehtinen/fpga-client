import os
import tkinter as tk
import numpy
import io
from PIL import ImageTk,Image

workdir_path = os.path.abspath(os.getcwd())
input_images_folder = 'input-images'
output_images_folder = 'output-images'

def get_input_image_by_name(name):
    img_path = os.path.join(workdir_path, input_images_folder, name)
    img = Image.open(img_path)

    return img

def get_output_image(name):
    return ''

def list_directory(path):
    if (path and len(path)):
        return os.listdir(path)
    
    return os.listdir()

def get_input_images_list():
    img_list = list_directory(input_images_folder)
    
    if not (img_list and len(img_list)):
        print("No input images found")
        return []
    
    return img_list

def get_output_images_list():
    img_list = list_directory(output_images_folder)
    
    if not (img_list and len(img_list)):
        print("No output images found")
        return []
    
    return img_list

def resize_image(img):
    width, height = img.size

    if width > 1000 or height > 1000:
        img = img.resize((width//2, height//2))
    
    return img

def get_input_images():
    img_list = list_directory(input_images_folder)
    
    if not (img_list and len(img_list)):
        print("No input images found")
        return []
    
    images = []

    for img in img_list:
        img_path = os.path.join(workdir_path, input_images_folder, img)
        img_o = Image.open(img_path)
        img_o = resize_image(img_o)
        
        images.append(ImageTk.PhotoImage(img_o))

    return images

def get_output_images():
    img_list = list_directory(output_images_folder)

    if not (img_list and len(img_list)):
        print("No output images found")
        return []

    images = []

    for img in img_list:
        img_path = os.path.join(workdir_path, output_images_folder, img)
        img_o = Image.open(img_path)
        w, h = img_o.size
        
        if w > 1000 or h > 1000:
            img_o = img_o.resize((w//2, h//2))
        
        images.append(ImageTk.PhotoImage(img_o))

    return images
        
