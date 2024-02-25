from customtkinter import CTkButton

def button(parent, command, icon = None, fg_color="black", text=''):
    button = CTkButton(parent, fg_color=fg_color, text=text, command=command)
    
    if icon:
        button.configure(image=icon)
        
    button.pack(side="left", padx=5, pady=5)
    return button