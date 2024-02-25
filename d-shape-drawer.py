import tkinter as tk
from PIL import Image, ImageTk


class ShapeDrawerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shape Drawer")

        self.canvas = tk.Canvas(root, width=700, height=200, bg="yellow")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.shape_type_var = tk.StringVar()
        self.shape_type_var.set("Circle")

        self.color_var = tk.StringVar()
        self.color_var.set("Black")

        self.size_var = tk.DoubleVar()
        self.size_var.set(20.0)

        self.create_widgets()

        self.start_x = None
        self.start_y = None

    def create_widgets(self):
        
         # Custom color buttons
        black_button = tk.Button(self.root, text=" ", bg="black", width=8, relief=tk.RAISED, command=lambda: self.color_var.set("Black"))
        black_button.pack(side=tk.LEFT, padx=5)
        red_button = tk.Button(self.root, text=" ", bg="red", width=8, relief=tk.RAISED, command=lambda: self.color_var.set("Red"))
        red_button.pack(side=tk.LEFT, padx=5)
        green_button = tk.Button(self.root, text=" ", bg="green", width=8, relief=tk.RAISED, command=lambda: self.color_var.set("Green"))
        green_button.pack(side=tk.LEFT, padx=5)
        blue_button = tk.Button(self.root, text=" ", bg="blue", width=8, relief=tk.RAISED, command=lambda: self.color_var.set("Blue"))
        blue_button.pack(side=tk.LEFT, padx=5)
        

        color_label = tk.Label(self.root, text="Color:")
        color_label.pack(side=tk.LEFT, padx=25)
        

        color_option_menu = tk.OptionMenu(self.root, self.color_var, "Black", "Red", "Green", "Blue")
        color_option_menu.pack(side=tk.LEFT, padx=25)
        
        shape_label = tk.Label(self.root, text="Shape:")
        shape_label.pack(side=tk.LEFT, padx=25)

        shape_option_menu = tk.OptionMenu(self.root, self.shape_type_var, "Circle", "Rectangle", "Line", "Triangle")
        shape_option_menu.pack(side=tk.LEFT, padx=25)

        size_label = tk.Label(self.root, text="Size:")
        size_label.pack(side=tk.LEFT, padx=25)

        size_scale = tk.Scale(self.root, from_=5.0, to=50.0, orient=tk.HORIZONTAL, variable=self.size_var)
        size_scale.pack(side=tk.LEFT, padx=25)

        clear_button_icon = Image.open("icon.png")  # Change "clear_icon.png" to your clear icon file
        clear_button_photo = ImageTk.PhotoImage(clear_button_icon)
        clear_button = tk.Button(self.root, image=clear_button_photo,text="Clear Canvas", command=self.clear_canvas)
        clear_button.image = clear_button_photo
        clear_button.pack(side=tk.LEFT, padx=25)

        

        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        

    def on_mouse_click(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        shape = self.shape_type_var.get()
        color = self.color_var.get()
        size = self.size_var.get()

        if shape == "Circle":
            self.canvas.delete("circle_preview")
            radius = abs(event.x - self.start_x)  # Calculate radius based on mouse movement
            self.canvas.create_oval(self.start_x - radius, self.start_y - radius,
                                     self.start_x + radius, self.start_y + radius,
                                     fill=color, tags="circle_preview")
        elif shape == "Rectangle":
            self.canvas.delete("rectangle_preview")
            center = abs(event.x - self.start_x)
            self.canvas.create_rectangle(self.start_x - center, self.start_y - center, event.x, event.y,
                                         fill=color, tags="rectangle_preview")
        elif shape == "Line" :
            self.canvas.delete("line_preview")
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                             fill=color, tags="line_preview")
        elif shape == "Triangle":
            self.canvas.delete("triangle_preview")
            x1, y1 = self.start_x, event.y
            x2, y2 = event.x, event.y
            x3, y3 = (self.start_x + event.x) // 2, self.start_y
            self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, tags="triangle_preview")

        self.selected_shape_id = self.selected_shape
        
        
    def clear_canvas(self):
        self.canvas.delete("all")


def main():
    root = tk.Tk()
    app = ShapeDrawerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
