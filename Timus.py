# Importing modules
import tkinter as tk       
import pathlib
import os
import random
import time

# Creating global functions
def getfilepath(filename):
    """This function returns the filepath of the given filename

    Args:
        filename (string): the name of the file (e.g. "image.png")

    Returns:
        string: the filepath of the given filename (e.g. "C:/Users/User/Desktop/image.png")
    """
    current_dir = pathlib.Path(__file__).parent.resolve() # This gets the current directory where the program is running
    current_dir = os.path.join(current_dir, "assets/") # Joins this filepath with the assets folder
    img_path = os.path.join(current_dir, filename) # Joins this filepath with the filename
    return img_path # Returns the complete filepath

# Creating global variables
seeninstructions = False # This variable is used to check if the instructions have been seen since the program has run
highscore = 0 # This variable is used to store the highscore
maxwindows = 20 # This variable is used to set the maximum number of windows that can be opened at once
windowscreateduponmistake = 2 # This variable is used to set the number of windows that are created when the user makes a mistake
maxwindowtimer = 15 # This variable is used to set the maximum time that a window can be open for

# Creating the Game window class 
class GameWindow:
    """This class is used to create each game window
    """
    def __init__(self):
        # Create window
        self.root = tk.Tk()
        self.root.title("TIMUS")

        # Finds out users screen size
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()

        # Randomizes the size of the window which is to be created
        windowwidth = random.randint(100, 500)
        windowheight = random.randint(100, 350)

        # Figures out where to place the window on the screen so that the window is not off the screen
        xpos = random.randint(0, screenwidth - windowwidth)
        ypos = random.randint(0, screenheight - windowheight)

        # Places the window on the screen at this location
        self.root.geometry(f"{windowwidth}x{windowheight}+{xpos}+{ypos}")

        # Disables the resizing of the window
        self.root.resizable(False, False)

        # Forces the game window to be on top of all other currently open windows
        self.root.attributes("-topmost", True)

        # Set window close action to close all currently open windows
        self.root.protocol("WM_DELETE_WINDOW",lambda: MainMenu.del_windows(MainMenu))

        # Binds a click on the window to the click() function
        self.root.bind("<Button-1>", self.click)

        # Determines the amount of time to click on the window (random betwwen 4 and 16 seconds)
        self.starttime = time.time()
        self.runtime = random.randint(4, maxwindowtimer)
        self.endtime = self.starttime + self.runtime
        self.timeleft = self.endtime - time.time()

        # Creates and places a label which will display the amount of time left
        self.label = tk.Label(self.root, text=str(self.timeleft), font=("Trebuchet MS", 50))
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Begins by ruuning the loop() fuinction immediately
        self.loop()

    # Creates a loop function which will run every 100ms for this window
    def loop(self):
        # Updates the amount of time left on the label
        self.timeleft = self.endtime - time.time()
        timeleft = round(self.timeleft, 1)
        self.label.config(text=str(timeleft))
        
        if timeleft > 5: # If the time left is greater than 5, set background of window and label to green
            self.label.config(bg="green")
            self.root.config(bg="green")
        elif timeleft > 3: # If the time left is greater than 3, set background of window and label to yellow
            self.label.config(bg="yellow")
            self.root.config(bg="yellow")
        elif timeleft > 1: # If the time left is greater than 1, set background of window and label to red
            self.label.config(bg="red")
            self.root.config(bg="red")
        elif timeleft > 0: # If the time left is greater than 0, set background of window and label to black and the text color to white
            self.label.config(bg="black", fg="white")
            self.root.config(bg="black")
        else: # If the time left is less than 0 (if the user does not click on the window in time), run the delete_self() function and open two more game windows
            self.delete_self()
            for i in range (windowscreateduponmistake):
                MainMenu.add_window(MainMenu)
        
        # Runs the loop() function again after 100ms
        self.root.after(100, self.loop)

    # Creates a function which will run every time the user clicks within the window
    def click(self, event):
        global highscore
        if self.timeleft < 1: # If the time left is less that 1, run the delete_self() function
            self.delete_self()
            MainMenu.score+=10
            if MainMenu.windowcount == 0: # If there are no windows left open, add score and return to the main menu 
                if MainMenu.score > highscore:
                    highscore = MainMenu.score
                MainMenu.del_windows(MainMenu)
                application = MainMenu()
                
        else: # If the user clicks when the timer is not < 1 second, run the delete_self() function and open 2 more windows
            self.delete_self()
            for i in range (windowscreateduponmistake):
                MainMenu.add_window(MainMenu)

    # Create a function which will run when the window is to be deleted
    def delete_self(self):
        self.root.destroy() # Delete the current window
        MainMenu.windowcount -= 1 # Reduce the amount of windows open by 1

# Creating the Instructions window class  
class Instructions:
    """This class is used to create the instructions window
    """
    def __init__(self, afteraction):
        global seeninstructions
        
        self.action = afteraction

        # Create window
        self.root = tk.Tk()
        self.root.title("TIMUS")

        # Sets the size of the window to 600 by 400 pixels
        self.root.geometry("600x400")
        
        # Sets the minimum size that the main menu window can be resized to as 600 by 400 pixels
        self.root.minsize(600, 400)

        # Creates a frame within the window and grids it
        content = tk.Frame(self.root, padx=12, pady=12, bg="#ff0000")
        content.grid(column=0, row=0, sticky = "nsew")
        
        # Recieves the title image from the assets folder and places in on the window
        titleimage= tk.PhotoImage(file=getfilepath("instructionstitle.png"))
        titlelabel = tk.Label(content, image=titleimage, bg="#ff0000", padx=5, pady=5)
        titlelabel.grid(row=0, column=0, columnspan=5, sticky = "nsew", padx=5, pady=5)

        # Creates a label which will display the instructions
        instructionsblurbimage= tk.PhotoImage(file=getfilepath("instructionsblurb.png"))
        instructionsblurblabel = tk.Label(content, borderwidth=10, background="white", relief="groove", image=instructionsblurbimage)
        instructionsblurblabel.grid(row=1, column=2, sticky = "nsew", padx=5, pady=5)

        # Creates a button which will return to the main menu window or start the game depending if the user has read the instructions 
        doneimage = tk.PhotoImage(file=getfilepath("done.png"))
        backbutton = tk.Button(content, borderwidth=10, background="white", relief="groove", image=doneimage)
        if self.action == "start":
            backbutton.config(command=lambda: self.start_game(self))
        elif self.action == "mainmenu":
            backbutton.config(command=lambda: self.return_to_main_menu(self))
        backbutton.grid(row=2, column=2, sticky = "nsew", padx=5, pady=5)

        # Set window close action to return to main menu rather than close the program
        self.root.protocol("WM_DELETE_WINDOW",lambda: self.return_to_main_menu(self))

        # Sets the seeninstructions variable to true
        seeninstructions = True

        # Configure all columns and rows within the instructions window to expand to fill the window if resized
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        for i in range (0, 5):
            content.columnconfigure(i, weight=1)
        for i in range (0, 3):
            content.rowconfigure(i, weight=1)

        self.root.mainloop()
    
    # Creates a function which is to be run when the user clicks the back button from clicking on the instructions
    def return_to_main_menu(self, event):
        self.root.destroy()
        application = MainMenu()
    
    def start_game(self, event):
        self.root.destroy()
        MainMenu.add_window(MainMenu)

# Creating the Settings window class  
class Settings:
    """This class is used to create the Settings window
    """
    def __init__(self):
        # Create window
        self.root = tk.Tk()
        self.root.title("TIMUS")

        # Sets the size of the window to 600 by 400 pixels
        self.root.geometry("600x400")
        
        # Sets the minimum size that the settings window can be resized to as 600 by 400 pixels
        self.root.minsize(600, 400)

        # Creates a frame within the window and grids it
        content = tk.Frame(self.root, padx=12, pady=12, bg="#ff0000")
        content.grid(column=0, row=0, sticky = "nsew")
        
        # Recieves the title image from the assets folder and places in on the window
        titleimage= tk.PhotoImage(file=getfilepath("settingstitle.png"))
        titlelabel = tk.Label(content, image=titleimage, bg="#ff0000", padx=5, pady=5)
        titlelabel.grid(row=0, column=0, columnspan=4, sticky = "nsew", padx=5, pady=5)

        # Creates a list of settings which are to be created
        settinglabels = ["maxopenwindows", "createduponmistake", "maxtimer"]
        
        # Creates a list of images and spinboxes are to be used for the settings
        images = []
        self.spinboxes = []

        # For each button in the list of buttons, do the following
        for index, settinglabels in enumerate(settinglabels):
            # Add the appropriate image to the list of images so that the image is stored in memory
            images.append(tk.PhotoImage(file=getfilepath(settinglabels + ".png")))
            
            settinglabel = tk.Label(content, borderwidth=10, background="white", relief="groove", image=images[index])
            settinglabel.grid(row=index+1, column=0, columnspan=2, sticky = "nsew", padx=5, pady=5)
            settingsspinbox = tk.Spinbox(content, from_=1, to=999999, width=3, wrap=True, font=("Trebuchet MS bold", 20), borderwidth=10, background="white", relief="groove", validate= "key")
            if index == 0:
                settingsspinbox.config(value=maxwindows)
            elif index == 1:
                settingsspinbox.config(value=windowscreateduponmistake)
            elif index == 2:
                settingsspinbox.config(value=maxwindowtimer)

            settingsspinbox["validatecommand"] = (settingsspinbox.register(self.testVal),"%P","%d")
            self.spinboxes.append(settingsspinbox)
            settingsspinbox.grid(row=index+1, column=3, sticky = "nsew", padx=5, pady=5)

        # Creates a button which will reset all settings to default
        settodefaultimage= tk.PhotoImage(file=getfilepath("settodefault.png"))
        settodefaultbutton = tk.Button(content, borderwidth=10, background="white", relief="groove", image=settodefaultimage, command=lambda: self.reset_to_default())
        settodefaultbutton.grid(row=4, column=0, columnspan=4, sticky = "nsew", padx=5, pady=5)

        # Creates a button which will return to the main menu window 
        doneimage = tk.PhotoImage(file=getfilepath("done.png"))
        backbutton = tk.Button(content, borderwidth=10, background="white", relief="groove", image=doneimage, command=lambda: self.return_to_main_menu())
        backbutton.grid(row=5, column=0, columnspan=4, sticky = "nsew", padx=5, pady=5)

        # Set window close action to return to main menu rather than close the program
        self.root.protocol("WM_DELETE_WINDOW",lambda: self.return_to_main_menu())

        # Configure all columns and rows within the instructions window to expand to fill the window if resized
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        for i in range (0, 4):
            content.columnconfigure(i, weight=1)
        for i in range (0, 7):
            content.rowconfigure(i, weight=1)

        self.root.mainloop()
    
    def testVal(self, characteradded, action):
        if action == "1": # If the action is insert character
            if not characteradded.isdigit(): # If the character is not a digit
                return False # Return false and allow character to be typed
        return True # Return true and allow character to be typed

    def reset_to_default(self):
        global maxwindows
        global windowscreateduponmistake
        global maxwindowtimer

        maxwindows = 20
        windowscreateduponmistake = 2
        maxwindowtimer = 15
        self.root.destroy()
        application.settings = Settings()

    # Creates a function which is to be run when the user clicks the back button from clicking on the instructions
    def return_to_main_menu(self):
        global maxwindows
        global windowscreateduponmistake
        global maxwindowtimer
        maxwindows = int(self.spinboxes[0].get())
        windowscreateduponmistake = int(self.spinboxes[1].get())
        maxwindowtimer = int(self.spinboxes[2].get())
        self.root.destroy()
        application = MainMenu()

# Creating the Main Menu class
class MainMenu:
    """This class is used to create the Main Menu window
    """
    def __init__(self):
        # Create window
        self.root = tk.Tk()
        self.root.title("TIMUS")

        # Sets the size of the window to 600 by 400 pixels
        self.root.geometry("600x400")
        
        # Sets the minimum size that the main menu window can be resized to as 300 by 400 pixels
        self.root.minsize(300, 400)

        # Creates a frame within the window and grids it
        content = tk.Frame(self.root, padx=12, pady=12, bg="#ff0000")
        content.grid(column=0, row=0, sticky = "nsew")
        
        # Recieves the title image from the assets folder and places in on the window
        titleimage= tk.PhotoImage(file=getfilepath("title.png"))
        titlelabel = tk.Label(content, image=titleimage, bg="#ff0000")
        titlelabel.grid(row=0, column=0, rowspan=2, columnspan=5, sticky = "nsew")

        # Creates a label underneath the title which will display the user"s high score
        scoretext = "High Score: " + str(highscore)
        scorelabel = tk.Label(content, borderwidth=10, background="white", relief="groove", text=scoretext, font=("Trebuchet MS bold", 12))
        scorelabel.grid(row=2, column=2, sticky = "nsew", padx=5, pady=5)

        # Creates a list of buttons which are to be created
        buttonlabels = ["start", "instructions", "settings", "quit"]
        
        # Creates a list of images which are to be used for the buttons
        images = []

        # For each button in the list of buttons, do the following
        for index, buttonlabel in enumerate(buttonlabels):
            # Add the appropriate image to the list of images so that the image is stored in memory
            images.append(tk.PhotoImage(file=getfilepath(buttonlabel + ".png")))
            
            # Create a button with this image
            button = tk.Button(content, borderwidth=10, background="white", relief="groove", image=images[index])
        
            # Configures the command on the button to run the appropriate function
            if buttonlabel == "start": # If the button is the start button, set the command to run the start() function
                button.config(command=lambda: self.start())
            elif buttonlabel == "instructions":# If the button is the instructions button, set the command to run the instructions() function
                button.config(command=lambda: self.instructions("mainmenu"))
            elif buttonlabel == "settings": # If the button is the settings button, set the command to run the settings() function
                button.config(command=lambda: self.settings())
            elif buttonlabel == "quit": # If the button is the quit button, set the command to close the main menu
                button.config(command=lambda: self.root.destroy())

            # Place the button in descending order in the main menu window
            button.grid(column=2, row=index + 3, sticky = "nsew", padx=5, pady=5)

        # Configure all columns and rows within the main menu window to expand to fill the window if resized
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        for i in range (0, 5):
            content.columnconfigure(i, weight=1)
        for i in range (0, 6):
            content.rowconfigure(i, weight=1)

        # Creates a variable which will store the amount of windows open
        MainMenu.windowcount = 0        

        # Create a list of all windows which are currently open
        MainMenu.windows = []

        # Permanently loop the main menu window 
        self.root.mainloop()
    
    # Creates a function which will run when the start button is clicked
    def start(self):
        MainMenu.score = 0
        if seeninstructions == True:
            self.root.destroy()
            self.add_window()
        elif seeninstructions == False:
            # start the instructions window and after reading the instructions start the game
            self.instructions("start")

    # Creates a function which will run when the instructions button is clicked
    def instructions(self, afteraction):
        self.root.destroy()
        self.instructions = Instructions(afteraction)

    # Creates a function which will run when the start button is clicked
    def settings(self):
        self.root.destroy()
        self.settings = Settings()

    # Creates a function which will run when a window is to be added
    def add_window(self):
        if MainMenu.windowcount < maxwindows:
            # Create a new window by creating a new window instance
            window = GameWindow()
            # Save this Window to the list of windows
            MainMenu.windows.append(window)
            # Increase the amount of windows open by 1
            MainMenu.windowcount += 1
        else:
            MainMenu.score-=10

    # Creates a function which will run when all windows are to be deleted
    def del_windows(self):
        # For each windows in the list of windows
        for window in MainMenu.windows:
            try:
                # Delete that window
                window.root.destroy()
            except:
                continue
        # Open the main menu
        application = MainMenu()

# Starts the main menu
application = MainMenu()