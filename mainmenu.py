# importing modules
import tkinter as tk       
import pathlib
import os

# creating helper functions
def get_image_path(filename):
    current_dir = pathlib.Path(__file__).parent.resolve() # current directory
    current_dir = os.path.join(current_dir, "assets/") # join with assets folder
    img_path = os.path.join(current_dir, filename) # join with your image's file name
    return img_path

# setting up window
root = tk.Tk()
root.title('TIMUS')    
root.geometry('600x400')

content = tk.Frame(root, padx=12, pady=12, bg='#ff0000')
content.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

titleimage= tk.PhotoImage(file=get_image_path("title.png"))
titlelabel = tk.Label(content, image=titleimage, bg='#ff0000')
titlelabel.grid(row=0, column=0, rowspan=2, columnspan=5, sticky=tk.N+tk.S+tk.E+tk.W)

startimage = tk.PhotoImage(file=get_image_path("Start.png"))
startbutton = tk.Button(content, borderwidth = 10, background = 'white', relief = 'groove', image=startimage, height=1, command=lambda: root.destroy())
startbutton.grid(row=2, column=2, rowspan=1, columnspan= 1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

instructionsimage = tk.PhotoImage(file=get_image_path("Instructions.png"))
instructionsbutton = tk.Button(content, borderwidth = 10, background = 'white', relief = 'groove', image=instructionsimage, height=1, command=lambda: root.destroy())
instructionsbutton.grid(row=3, column=2, rowspan=1, columnspan= 1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

settingsimage = tk.PhotoImage(file=get_image_path("settings.png"))
settingsbutton = tk.Button(content, borderwidth = 10, background = 'white', relief = 'groove', image=settingsimage, height=1, command=lambda: root.destroy())
settingsbutton.grid(row=4, column=2, rowspan=1, columnspan= 1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

quitimage = tk.PhotoImage(file=get_image_path("Quit.png"))
quitbutton = tk.Button(content, borderwidth = 10, background = 'white', relief = 'groove', image=quitimage, height=1, command=lambda: root.destroy())
quitbutton.grid(row=5, column=2, rowspan=1, columnspan= 1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

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
