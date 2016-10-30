import numpy as np
import PIL 
from PIL import Image
from os import listdir
from os.path import isfile, join
import Image

def resize_image(directoryname):
    """
    Resizes all images in the directory
    """
    size = 125,125
    files_list = [f for f in listdir(directoryname) if isfile(join(directoryname, f))]
    for f in files_list:
        im = Image.open(directoryname + "/" + f)
        im = im.resize(size,Image.ANTIALIAS)
        im.save(directoryname + "/exp/" + f,"JPEG")

if __name__ == "__main__":
    directoryname = "../Data/Book_Covers"
    resize_image(directoryname)
