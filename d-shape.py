import tkinter as tk

# Function to draw a shape based on user input
def draw_shape():
    shape = selected_shape.get()
    x1 = int(x1_entry.get())
    y1 = int(y1_entry.get())
    x2 = int(x2_entry.get())
    y2 = int(y2_entry.get())
    
    if shape == "Rectangle":
        canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
    elif shape == "Oval":
        canvas.create_oval(x1, y1, x2, y2, fill="red")
    elif shape == "Line":
        canvas.create_line(x1, y1, x2, y2, fill="yellow")

# Function to clear the canvas
def clear_canvas():
    canvas.delete("all")

# Create the main application window
root = tk.Tk()
root.title("Shapes GUI")

# Create a canvas widget
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# Create a label for shape selection
shape_label = tk.Label(root, text="Select Shape:")
shape_label.pack()

# Dropdown menu for shape selection
shapes = ["Rectangle", "Oval", "Line"]
selected_shape = tk.StringVar(root)
selected_shape.set(shapes[0])
shape_menu = tk.OptionMenu(root, selected_shape, *shapes)
shape_menu.pack()

# Create labels and entry widgets for shape parameters
param_label = tk.Label(root, text="Enter Parameters:")
param_label.pack()

x1_label = tk.Label(root, text="X1:")
x1_label.pack()
x1_entry = tk.Entry(root)
x1_entry.pack()

y1_label = tk.Label(root, text="Y1:")
y1_label.pack()
y1_entry = tk.Entry(root)
y1_entry.pack()

x2_label = tk.Label(root, text="X2:")
x2_label.pack()
x2_entry = tk.Entry(root)
x2_entry.pack()

y2_label = tk.Label(root, text="Y2:")
y2_label.pack()
y2_entry = tk.Entry(root)
y2_entry.pack()

# Create button for drawing shapes
draw_button = tk.Button(root, text="Draw Shape", command=draw_shape)
draw_button.pack()

# Create button for clearing the canvas
clear_button = tk.Button(root, text="Clear Canvas", command=clear_canvas)
clear_button.pack()

# Run the Tkinter event loop
root.mainloop()
