from customtkinter import CTkButton, CTkImage

from PIL import Image




class ImageButton(CTkButton):
    def __init__(self, master, image_path, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        image = Image.open(fp=image_path)
        icon= CTkImage(size=(70, 70), light_image=image, dark_image=image)
        
        self.configure(image=icon, text="", height=0, width=0, corner_radius= 3)
        

          