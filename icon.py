from customtkinter import CTkImage
from PIL import Image

def icon_builder(file_path):
    path = Image.open(fp=file_path)
    return CTkImage(size=(25, 25), light_image=path, dark_image=path)
