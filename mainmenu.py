# importing modules
import tkinter as tk       
import pathlib
import os

# creating helper functions
def getimagepath(filename):
    current_dir = pathlib.Path(__file__).parent.resolve() # current directory
    current_dir = os.path.join(current_dir, "assets/") # join with assets folder
    img_path = os.path.join(current_dir, filename) # join with your image's file name
    return img_path

#creating gui functions
def start():
    print("Start")

def instructions():
    print("Instructions")

def settings():
    print("Settings")

# setting up window
root = tk.Tk()
root.title('TIMUS')    
root.geometry('600x400')

content = tk.Frame(root, padx=12, pady=12, bg='#ff0000')
content.grid(column=0, row=0, sticky = "nsew")

titleimage= tk.PhotoImage(file=getimagepath("title.png"))
titlelabel = tk.Label(content, image=titleimage, bg='#ff0000')
titlelabel.grid(row=0, column=0, rowspan=2, columnspan=5, sticky = "nsew")

# iterates through list of buttons, selecs the image, and creates a button for each
buttonlabels = ["start", "instructions", "settings", "quit"]
images = []
for index, buttonlabel in enumerate(buttonlabels):
    images.append(tk.PhotoImage(file=getimagepath(buttonlabel + ".png")))
    button = tk.Button(content, borderwidth=10, background="white", relief="groove", image=images[index], command=lambda: root.destroy())
 
    # checks each button label assigns an appropriate command
    if buttonlabel == "start":
        # configure the button to run the start function
        button.config(command=lambda: start())
    elif buttonlabel == "instructions":
        # configure the button to run the instructions function
        button.config(command=lambda: instructions())
    elif buttonlabel == "settings":
        # configure the button to run the settings function
        button.config(command=lambda: settings())

    button.grid(column=2, row=index + 2, sticky = "nsew", padx=5, pady=5)

# configuring all rows and columns for resizing
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
for i in range (0, 5):
    content.columnconfigure(i, weight=1)
for i in range (0, 6):
    content.rowconfigure(i, weight=1)

# looping
while True:
    root.update()