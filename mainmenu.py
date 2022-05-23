# importing modules
import tkinter as tk       
import pathlib
import os

# creating global functions
def getimagepath(filename):
        current_dir = pathlib.Path(__file__).parent.resolve() # current directory
        current_dir = os.path.join(current_dir, "assets/") # join with assets folder
        img_path = os.path.join(current_dir, filename) # join with your image's file name
        return img_path

class Game:
    def __init__(self):
        print("GameGUI")

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

        # looping
        while True:
            self.root.update()

    # creating gui functions
    def start(self):
        self.game = Game()
        self.root.destroy()

    def instructions(self):
        self.instructions = Instructions()
        self.root.destroy()

    def settings(self):
        self.settings = Settings()
        self.root.destroy()

# starts the main menu
application = MainMenu()