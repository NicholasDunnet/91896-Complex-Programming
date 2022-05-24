# importing modules
import tkinter as tk       
import pathlib
import os
import random
from turtle import position

# creating global functions
def getimagepath(filename):
        current_dir = pathlib.Path(__file__).parent.resolve() # current directory
        current_dir = os.path.join(current_dir, "assets/") # join with assets folder
        img_path = os.path.join(current_dir, filename) # join with your image's file name
        return img_path

class GameWindow:
    def __init__(self):
        # Create window
        self.root = tk.Tk()
        self.root.title('TIMUS')

        # Finds out users screen size
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()

        # Randomizes the size of the window which is to be created
        windowwidth = random.randint(100, 500)
        windowheight = random.randint(100, 350)

        # Figures out where to place the window on the screen
        xpos = random.randint(0, screenwidth - windowwidth)
        ypos = random.randint(0, screenheight - windowheight)

        # Places the window on the screen and disables resizing of windows
        self.root.geometry(f"{windowwidth}x{windowheight}+{xpos}+{ypos}")
        self.root.resizable(False, False)

        # Set window close action to close all windows
        self.root.protocol("WM_DELETE_WINDOW",lambda: MainMenu.del_windows(MainMenu))

        # Allows the window to function with other windows and not be blocked
        self.root.after(1000, self.loop)

    # Creates a loop which will run every second for each window
    def loop(self):
        self.root.after(1000, self.loop)
        
class Instructions:
    def __init__(self):
        print("SettingsGUI")

class Settings:
    def __init__(self):
        print("SettingsGUI")

class MainMenu:
    def __init__(self):
        # setting up window
        self.root = tk.Tk()
        self.root.title('TIMUS')    
        self.root.geometry('600x400')
        self.root.minsize(300, 400)

        content = tk.Frame(self.root, padx=12, pady=12, bg='#ff0000')
        content.grid(column=0, row=0, sticky = "nsew")

        titleimage= tk.PhotoImage(file=getimagepath("title.png"))
        titlelabel = tk.Label(content, image=titleimage, bg='#ff0000')
        titlelabel.grid(row=0, column=0, rowspan=2, columnspan=5, sticky = "nsew")

        # iterates through list of buttons, selecs the image, and creates a button for each
        buttonlabels = ["start", "instructions", "settings", "quit"]
        images = []
        for index, buttonlabel in enumerate(buttonlabels):
            images.append(tk.PhotoImage(file=getimagepath(buttonlabel + ".png")))
            button = tk.Button(content, borderwidth=10, background="white", relief="groove", image=images[index], command=lambda: self.root.destroy())
        
            # checks each button label assigns an appropriate command
            if buttonlabel == "start":
                # configure the button to run the start function
                button.config(command=lambda: self.start())
            elif buttonlabel == "instructions":
                # configure the button to run the instructions function
                button.config(command=lambda: self.instructions())
            elif buttonlabel == "settings":
                # configure the button to run the settings function
                button.config(command=lambda: self.settings())

            button.grid(column=2, row=index + 2, sticky = "nsew", padx=5, pady=5)

        # configuring all rows and columns for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        for i in range (0, 5):
            content.columnconfigure(i, weight=1)
        for i in range (0, 6):
            content.rowconfigure(i, weight=1)

        # Create array of windows.
        MainMenu.windows = []

        # looping
        self.root.mainloop()

    def start(self):
        self.add_window()
        # self.root.destroy()

    def instructions(self):
        self.instructions = Instructions()
        self.root.destroy()

    def settings(self):
        self.settings = Settings()
        self.root.destroy()

    def add_window(self):
        # Create a new window by creating a new Window instance.
        w = GameWindow()
        # Save this Window to the list of windows.
        MainMenu.windows.append(w)

    def del_windows(self):
        # Close all windows.
        for window in MainMenu.windows:
            try:
                window.root.destroy()
            except:
                continue
        application = MainMenu()

# starts the main menu
application = MainMenu()