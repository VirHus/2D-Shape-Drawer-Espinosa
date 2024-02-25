import customtkinter
from button_builder import button
from icon import icon_builder
from tkinter import *
from tkinter import ttk
from tkinter.constants import *
from tkinter import colorchooser
from PIL import Image, ImageTk
import math
from customtkinter import CTkImage


class DShapeDrawerApp(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("D Shape Drawer")
        self.geometry('1000x600')
        self.resizable(True, True)

        # Create frame1
        frame1 = customtkinter.CTkFrame(master=self, height=200, fg_color="grey")
        frame1.pack(side="top",  fill="both", expand="True")

        # Create frame2
        frame2 = customtkinter.CTkFrame(master=self, height=30, fg_color="black")
        frame2.pack(fill="both")

        # Create frame3
        frame3 = customtkinter.CTkFrame(master=self, height=100, fg_color="white")
        frame3.pack(side="bottom", fill="both")

        # Button to select Rectangle
        button(frame3, command=lambda: self.set_shape("Rectangle"), image=icon_builder("black-square.png"))
        button(frame3, command=lambda: self.set_shape("Circle"), icon=icon_builder("black-circle.png"))
        button(frame3, command=lambda: self.set_shape("Triangle"), icon=icon_builder("bleach.png"))   
        
        

        # Canvas for drawing shapes
        self.canvas = customtkinter.CTkCanvas(frame1, bg="grey")
        self.canvas.pack(fill="both", expand=True)

        # Initialize color
        self.color = "black"
        


        # Button to open color picker
        self.color_picker_button = customtkinter.CTkButton(frame2, text="CHOOSE COLORS",command=self.open_color_picker)
        self.color_picker_button.pack(side="left")

        
        # Button to delete selected shape
        self.delete_button = customtkinter.CTkButton(frame2, text="Delete", command=self.delete_shape)
        self.delete_button.pack(side="right")
        # Bind canvas click event for drawing shapes
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.update_draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        
        # Bind arrow key events
        self.bind("<Up>", lambda event: self.move_shape_up())
        self.bind("<Down>", lambda event: self.move_shape_down())
        self.bind("<Left>", lambda event: self.move_shape_left())
        self.bind("<Right>", lambda event: self.move_shape_right())
        self.bind("<KeyPress>", self.handle_keypress)

        # Variables to store shape drawing parameters
        self.start_x = None
        self.start_y = None
        self.current_shape = None
        
        # Variables to store selected shape for deletion
        self.selected_shape_id = None
        
        # Default selected shape
        self.selected_shape = "Rectangle" 

        # Bind canvas click event to select shape
        self.canvas.bind("<Button-3>", self.select_shape)

    def open_color_picker(self):
        
        color = colorchooser.askcolor(title="Choose color")
        if color[1]:
            print("Selected color:", color[1])
            self.color = color[1]  # Update color
            
            if self.selected_shape_id:
                self.canvas.itemconfig(self.selected_shape_id, fill=self.color)
                
    def set_shape(self, shape):
        self.selected_shape = shape


    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y
        shape = self.selected_shape
        if shape == "Rectangle":
            self.current_shape = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, fill=self.color)
        elif shape == "Circle":
            self.current_shape = self.canvas.create_oval(event.x, event.y, event.x, event.y, fill=self.color)
        elif shape == "Triangle":
            self.current_shape = self.canvas.create_polygon(event.x, event.y, event.x, event.y, event.x, event.y, fill=self.color)

    def update_draw(self, event):
        if self.current_shape:
            if self.selected_shape != "Triangle":
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)
                self.canvas.coords(self.current_shape, 
                               self.start_x, self.start_y, 
                               event.x, self.start_y, 
                               event.x, event.y, 
                               self.start_x, event.y,
                               self.start_x, self.start_y)  # Close the octagon
            else:
                self.canvas.coords(self.current_shape, self.start_x, event.y, (self.start_x + event.x) // 2, self.start_y, event.x, event.y)
        
        
    def end_draw(self, event):
        self.current_shape = None
        
    def delete_shape(self):
        if self.selected_shape_id:
            self.canvas.delete(self.selected_shape_id)
            self.selected_shape_id = None
            self.canvas.delete("dot")  # Delete all dots

    def select_shape(self, event):
        x, y = event.x, event.y
        shape_ids = self.canvas.find_overlapping(x, y, x, y)
        if shape_ids:
            if self.selected_shape_id:
                self.canvas.delete("dot")  # Delete all dots
                self.canvas.itemconfig(self.selected_shape_id, outline="")
                
                
            self.selected_shape_id = shape_ids[-1]
            self.canvas.itemconfig(self.selected_shape_id, outline="white", width=4)
            
            bbox = self.canvas.bbox(self.selected_shape_id)
            corners = [(bbox[0], bbox[1]), (bbox[2], bbox[1]), (bbox[0], bbox[3]), (bbox[2], bbox[3])]
            for corner in corners:
                x, y = corner
                dot_radius = 3
                dot = self.canvas.create_oval(x - dot_radius, y - dot_radius, x + dot_radius, y + dot_radius, fill="white", tags="dot")
    
            # Check if Ctrl and "+" are pressed to increase the size of the shape
            if event.state & 0x4 and event.keysym == 'plus':
                self.canvas.scale(self.selected_shape_id, x, y, 1.1, 1.1)
                
        else:
            # Remove outline if no shape is selected
            if self.selected_shape_id:
                self.canvas.itemconfig(self.selected_shape_id, outline="")
                self.canvas.delete("dot")  # Delete all dots
            self.selected_shape_id = None
            
    def increase_size(self):
        if self.selected_shape_id:
            bbox = self.canvas.bbox(self.selected_shape_id)
            center_x = (bbox[0] + bbox[2]) / 2
            center_y = (bbox[1] + bbox[3]) / 2
            self.canvas.scale(self.selected_shape_id, center_x, center_y, 1.1, 1.1)
            

            
    def decrease_size(self):
        if self.selected_shape_id:
            bbox = self.canvas.bbox(self.selected_shape_id)
            center_x = (bbox[0] + bbox[2]) / 2
            center_y = (bbox[1] + bbox[3]) / 2
            self.canvas.scale(self.selected_shape_id, center_x, center_y, 0.9, 0.9)
            
    def move_shape_up(self):
        if self.selected_shape_id:
            self.canvas.move(self.selected_shape_id, 0, -10)

    def move_shape_down(self):
        if self.selected_shape_id:
            self.canvas.move(self.selected_shape_id, 0, 10)

    def move_shape_left(self):
        if self.selected_shape_id:
            self.canvas.move(self.selected_shape_id, -10, 0)

    def move_shape_right(self):
        if self.selected_shape_id:
            self.canvas.move(self.selected_shape_id, 10, 0)
            
    def handle_keypress(self, event):
    # Check if Ctrl, Shift, and + keys are pressed simultaneously
        if event.state & 0x4 and event.state & 0x1:
            if event.keysym == 'plus':
                self.increase_size()
            elif event.keysym == 'underscore':
                self.decrease_size()
            
if __name__ == "__main__":
    app = DShapeDrawerApp()
    app.mainloop()
