import json
from tkinter import filedialog, messagebox
import customtkinter
from ImageButton import ImageButton
from icon import icon_builder
from tkinter import *
from tkinter import ttk
from tkinter.constants import *
from tkinter import colorchooser
from PIL import Image, ImageTk
import math
from customtkinter import CTkImage

RECTANGLE = "RECTANGLE"
CIRCLE = "CIRCLE"
TRIANGLE = "TRIANGLE"
HEXAGON = "HEXAGON"
OCTAGON = "OCTAGON"
HEPTAGON = "HEPTAGON"

class DShapeDrawerApp(customtkinter.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("D Shape Drawer")
        self.geometry('1000x600')
        self.resizable(False, False)
        self.shapes = {}
        self.shape_size = {
            RECTANGLE: 0,
            CIRCLE: 0,
            TRIANGLE: 0,
            HEXAGON: 0,
            OCTAGON: 0,
            HEPTAGON: 0
        }
        
        
        
# Create frame1 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        frame1 = customtkinter.CTkFrame(master=self, height=200, fg_color="white")
        frame1.pack(side="top",  fill="both", expand="True")

# Create frame2 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        frame2 = customtkinter.CTkFrame(master=self, height=90, fg_color="orange")
        frame2.pack(fill="both")

# Create frame3 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        frame3 = customtkinter.CTkFrame(master=self, height=100, fg_color="black")
        frame3.pack(side="bottom", fill="both")

# Button to select SHAPES # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        rectangle = ImageButton(frame3, "shapes/square.png", command=lambda: self.set_shape(RECTANGLE), fg_color="orange")
        rectangle.pack(side="left", pady=5)
        rectangle.place(x=110, y=7)
        circle = ImageButton(frame3, "shapes/rec.png", command=lambda: self.set_shape(CIRCLE), fg_color="orange")
        circle.pack(side="left",pady=5)
        circle.place(x=240, y=7)
        triangle = ImageButton(frame3, "shapes/bleach (1).png", command=lambda: self.set_shape(TRIANGLE), fg_color="orange")   
        triangle.pack(side="left",pady=5)
        triangle.place(x=370, y=7)
        hexagon = ImageButton(frame3, "shapes/polygon.png", command=lambda: self.set_shape(HEXAGON), fg_color="orange")   
        hexagon.pack(side="left",pady=5)
        hexagon.place(x=500, y=7)
        octagon = ImageButton(frame3, "shapes/octagon.png", command=lambda: self.set_shape(OCTAGON), fg_color="orange")   
        octagon.pack(side="left",pady=5)
        octagon.place(x=630, y=7)
        heptagon = ImageButton(frame3, "shapes/heptagon.png", command=lambda: self.set_shape(HEPTAGON), fg_color="orange")   
        heptagon.pack(side="left",pady=5)
        heptagon.place(x=760, y=7)
        
        
        
        # Create the export button
        # export_button = customtkinter.CTkButton(self, text="Export", width=100, command=self.export_to_file)
        # export_button.pack(fill='both', pady=(5, 0), padx=5)

        # Create the import button
        # import_button = customtkinter.CTkButton(self, text="Import", width=100, command=self.import_from_file)
        # import_button.pack(fill='both', pady=(5, 0), padx=5)

        
        
        
        

# Canvas for drawing shapes # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.canvas = customtkinter.CTkCanvas(frame1, bg="white")
        self.canvas.pack(fill="both", expand=True)

# Initialize color # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.color = "black"
        
        
        self.angle = 0

# Button to open color picker # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        color_picker_button = ImageButton(frame2, "shapes/color-picker.png",command=self.open_color_picker, fg_color="black")
        color_picker_button.pack(side="left")
        color_picker_button.place(x=380, y=7)

        
# Button to delete selected shape # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        delete_button = ImageButton(frame2, "shapes/trash.png", command=self.delete_shape, fg_color="black")
        delete_button.pack(side="right")
        delete_button.place(x=540, y=7)
        
# Bind canvas click event for drawing shapes # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.update_draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)
        

        
# Bind arrow key events # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.bind("<Up>", lambda event: self.move_shape_up())
        self.bind("<Down>", lambda event: self.move_shape_down())
        self.bind("<Left>", lambda event: self.move_shape_left())
        self.bind("<Right>", lambda event: self.move_shape_right())
        self.bind("<KeyPress>", self.handle_keypress)
        # Bind canvas click event to select shape
        self.canvas.bind("<Button-3>", self.select_shape)



# Variables to store shape drawing parameters # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.start_x = None
        self.start_y = None
        self.current_shape = None
        
        self.start_coordinates = None
        self.end_coordinates = None
        self.angle = 0
        
        
# Variables to store selected shape for deletion # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        self.selected_shape_id = None
        
        # Default selected shape
        self.selected_shape = RECTANGLE 
        

# OPEN COLOR PICKER # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    def open_color_picker(self):
        
        color = colorchooser.askcolor(title="Choose color")
        if color[1]:
            print("Selected color:", color[1])
            self.color = color[1]  # Update color
        
            
            if self.selected_shape_id:
                self.canvas.itemconfig(self.selected_shape_id, fill=self.color)
                self.add_setting(self.selected_shape, "color", self.color)
                print(json.dumps(self.shapes,indent=4))
                
# CHOOSE A SHAPE # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
                
    def set_shape(self, shape):
        self.selected_shape = shape
        messagebox.showinfo("Shape Selected", f"You have selected {shape}")
        
    
    def add_shape(self,shape_name):
        self.shapes[shape_name] = {}
        
    def add_setting(self,shape_name, settings, value):
        if shape_name not in self.shapes:
            raise Exception("Shape not found")
        
        self.shapes[shape_name][settings] = value

# START DRAWING SHAPES # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    def start_draw(self, event):
        self.start_x = event.x
        self.start_y = event.y
        
        self.start_coordinates = (event.x, event.y)
        shape = self.selected_shape
        if shape == RECTANGLE:
            self.current_shape = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, fill=self.color) 
            self.add_shape(RECTANGLE)
            self.add_setting(RECTANGLE, "event_x", event.x)
            self.add_setting(RECTANGLE, "event_y", event.y)
            self.add_setting(RECTANGLE, "color", self.color)
            print(self.current_shape)
            
        elif shape == CIRCLE:
            self.current_shape = self.canvas.create_oval(event.x, event.y, event.x, event.y, fill=self.color)
            self.add_shape(CIRCLE)
            self.add_setting(CIRCLE, "event_x", event.x)
            self.add_setting(CIRCLE, "event_y", event.y)
            self.add_setting(CIRCLE, "color", self.color)
        elif shape == TRIANGLE:
            self.current_shape = self.canvas.create_polygon(event.x, event.y, event.x, event.y, event.x, event.y, fill=self.color)
            self.add_shape(TRIANGLE)
            self.add_setting(TRIANGLE, "event_x", event.x)
            self.add_setting(TRIANGLE, "event_y", event.y)
            self.add_setting(TRIANGLE, "color", self.color)
        elif shape == HEXAGON:
            self.current_shape = self.canvas.create_polygon(*self.hexagon_vertices(event.x, event.y,event.x, event.y), fill=self.color)
            self.add_shape(HEXAGON)
            self.add_setting(HEXAGON, "event_x", event.x)
            self.add_setting(HEXAGON, "event_y", event.y)
            self.add_setting(HEXAGON, "color", self.color)
        elif shape == OCTAGON:
            self.current_shape = self.canvas.create_polygon(*self.octagon_vertices(event.x, event.y, event.x, event.y), fill=self.color)
            self.add_shape(OCTAGON)
            self.add_setting(OCTAGON, "event_x", event.x)
            self.add_setting(OCTAGON, "event_y", event.y)
            self.add_setting(OCTAGON, "color", self.color)
        elif shape == HEPTAGON:
            self.current_shape = self.canvas.create_polygon(*self.heptagon_vertices(event.x, event.y, event.x, event.y), fill=self.color)
            self.add_shape(HEPTAGON)
            self.add_setting(HEPTAGON, "event_x", event.x)
            self.add_setting(HEPTAGON, "event_y", event.y)
            self.add_setting(HEPTAGON, "color", self.color)

        self.start_coordinates = (event.x, event.y)
        self.current_coordinates = (self.start_coordinates)
        
        
        
# DRAW POLYGON SHAPES # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        
    def hexagon_vertices(self, start_x, start_y, end_x, end_y):
        # Calculate the size of the hexagon based on the distance between start and end points
        size = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        
        # Calculate the center point of the hexagon
        self.center_x = (start_x + end_x) / 2
        self.center_y = (start_y + end_y) / 2

        vertices = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            vertex_x = self.center_x + size * math.cos(angle_rad)
            vertex_y = self.center_y + size * math.sin(angle_rad)
            vertices.extend([vertex_x, vertex_y])
        return vertices
    
    def octagon_vertices(self, start_x, start_y, end_x, end_y):
        # Calculate the size of the octagon based on the distance between start and end points
        size = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        
        # Calculate the center point of the octagon
        center_x = (start_x + end_x) / 2
        center_y = (start_y + end_y) / 2

        vertices = []
        for i in range(8):
            angle_deg = 45 * i
            angle_rad = math.radians(angle_deg)
            vertex_x = center_x + size * math.cos(angle_rad)
            vertex_y = center_y + size * math.sin(angle_rad)
            vertices.extend([vertex_x, vertex_y])
        return vertices
    
    def heptagon_vertices(self, start_x, start_y, end_x, end_y):
        # Calculate the size of the heptagon based on the distance between start and end points
        size = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        
        # Calculate the center point of the heptagon
        center_x = (start_x + end_x) / 2
        center_y = (start_y + end_y) / 2

        vertices = []
        for i in range(7):
            angle_deg = 360/7 * i  # Angle for each vertex
            angle_rad = math.radians(angle_deg)
            vertex_x = center_x + size * math.cos(angle_rad)
            vertex_y = center_y + size * math.sin(angle_rad)
            vertices.extend([vertex_x, vertex_y])
        return vertices
    
# UPDATE DRAW # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    
    def update_draw(self, event):
        if self.current_shape:
            if self.selected_shape == TRIANGLE:
                self.canvas.coords(self.current_shape, self.start_x, event.y, (self.start_x + event.x) // 2, self.start_y, event.x, event.y)
            elif self.selected_shape == HEXAGON:
                self.canvas.coords(self.current_shape, *self.hexagon_vertices(self.start_x, self.start_y, event.x, event.y))
            elif self.selected_shape == OCTAGON:
                self.canvas.coords(self.current_shape, *self.octagon_vertices(self.start_x, self.start_y, event.x, event.y))
            elif self.selected_shape == HEPTAGON:
                self.canvas.coords(self.current_shape, *self.heptagon_vertices(self.start_x, self.start_y, event.x, event.y))
            else:
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)

# END DRAW OR THE END POINT OF THE SHAPES# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  

    def end_draw(self, event):
        self.current_shape = None
        self.end_coordinates = (event.x, event.y)
    
        print(json.dumps(self.shapes,indent=4))
# DELETE SHAPES# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        
    def delete_shape(self):
        if self.selected_shape_id:
            self.canvas.delete(self.selected_shape_id)
            # Remove the shape from the array
            self.shapes = [shape for shape in self.shapes if shape['shape_id'] != self.selected_shape_id]
            self.selected_shape_id = None
            self.canvas.delete("dot")  # Delete all dots
            

# SELECT SHAPES# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
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
     
     
     
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # Increase and Decrease the size
    def increase_size(self):
        if self.selected_shape_id:
            bbox = self.canvas.bbox(self.selected_shape_id)
            center_x = (bbox[0] + bbox[2]) / 2
            center_y = (bbox[1] + bbox[3]) / 2
            self.canvas.scale(self.selected_shape_id, center_x, center_y, 1.1, 1.1)
            self.shape_size[self.selected_shape] += 1
            self.add_setting(self.selected_shape, "Shape_Size",self.shape_size)
            self.add_setting(self.selected_shape, "center_x", center_x)
            self.add_setting(self.selected_shape, "center_y", center_y)
            self.add_setting(self.selected_shape, "shape_id", self.selected_shape_id)
            print(json.dumps(self.shapes,indent=4))
            
    def decrease_size(self):
        if self.selected_shape_id:
            bbox = self.canvas.bbox(self.selected_shape_id)
            center_x = (bbox[0] + bbox[2]) / 2
            center_y = (bbox[1] + bbox[3]) / 2
            self.canvas.scale(self.selected_shape_id, center_x, center_y, 0.9, 0.9)
            self.shape_size[self.selected_shape] -= 1
            self.add_setting(self.selected_shape, "Shape_Size",self.shape_size)
            self.add_setting(self.selected_shape, "center_x", center_x)
            self.add_setting(self.selected_shape, "center_y", center_y)
            self.add_setting(self.selected_shape, "shape_id", self.selected_shape_id)
            print(json.dumps(self.shapes,indent=4))
            
    def handle_keypress(self, event):
        
    # Check if Ctrl, Shift, and + keys are pressed simultaneously
        if event.state & 0x4 and event.state & 0x1:
            if event.keysym == 'plus':
                self.increase_size()
            elif event.keysym == 'underscore':
                self.decrease_size()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            

    #Movements of shapes    
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
            
            
if __name__ == "__main__":
    app = DShapeDrawerApp()
    app.mainloop()
