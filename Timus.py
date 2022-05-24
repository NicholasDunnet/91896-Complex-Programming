# importing modules
import tkinter as tk       
import pathlib
import os
import random
import time

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

        self.root.attributes("-topmost", True)

        # Figures out where to place the window on the screen
        xpos = random.randint(0, screenwidth - windowwidth)
        ypos = random.randint(0, screenheight - windowheight)

        # Places the window on the screen and disables resizing of windows
        self.root.geometry(f"{windowwidth}x{windowheight}+{xpos}+{ypos}")
        self.root.resizable(False, False)

        # Set window close action to close all windows
        self.root.protocol("WM_DELETE_WINDOW",lambda: MainMenu.del_windows(MainMenu))

        self.root.bind('<Button-1>', self.click)

        self.starttime = time.time()
        self.runtime = random.randint(4, 16)
        self.endtime = self.starttime + self.runtime
        self.timeleft = self.endtime - time.time()

        self.label = tk.Label(self.root, text=str(self.timeleft), font=(None, 50))
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Allows the window to function with other windows and not be blocked
        self.loop()

    def click(self, event):
        if self.timeleft < 1:
            self.delete_self()
        else:
            self.delete_self()
            MainMenu.add_window(MainMenu)
            MainMenu.add_window(MainMenu)

    def delete_self(self):
        print(MainMenu.windowcount)
        self.root.destroy()
        MainMenu.windowcount -= 1

    # Creates a loop which will run every second for each window
    def loop(self):
        self.timeleft = self.endtime - time.time()
        timeleft = round(self.timeleft, 1)
        self.label["text"] = timeleft
        # if the time left is greater than 5 set background to green
        if timeleft > 5:
            self.label.config(bg='green')
            self.root.config(bg='green')
        # if the time left is less than 5 set background to yellow
        elif timeleft > 3:
            self.label.config(bg='yellow')
            self.root.config(bg='yellow')
        # if the time left is less than 3 set background to red
        elif timeleft > 1:
            self.label.config(bg='red')
            self.root.config(bg='red')
        elif timeleft > 0:
            self.label.config(bg='black', fg='white')
            self.root.config(bg='black')
        # if the time left is less than 0 close the window
        else:
            self.delete_self()
            MainMenu.add_window(MainMenu)
            MainMenu.add_window(MainMenu)
        self.root.after(50, self.loop)
        
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
        
        MainMenu.windowcount = 0

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
        self.root.destroy()

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
        self.windowcount += 1

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