# Importing modules
import tkinter as tk       
import pathlib, os, random, time, math

# Creating global functions
def get_file_path(filename):
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

def center(window):
    """This function centers the given window on the users screen

    Args:
        win (object): the window
    """
    
    # Updates the information of the window
    window.update_idletasks()
    
    # Gets the actual width of the window (frame included)
    width = window.winfo_width()
    frm_width = window.winfo_rootx() - window.winfo_x()
    win_width = width + 2 * frm_width
    
    # Gets the actual height of the window (titlebar included)
    height = window.winfo_height()
    titlebar_height = window.winfo_rooty() - window.winfo_y()
    win_height = height + titlebar_height + frm_width
    
    # Creates the x and y values of the window
    x = window.winfo_screenwidth() // 2 - win_width // 2
    y = window.winfo_screenheight() // 2 - win_height // 2

    # Places the window using these x and y values
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    # Stops the window flashing in the wrong location before being moved to center
    window.deiconify()

# Creating global variables
seen_instructions_state = False # This variable is used to check if the instructions have been seen since the program has run

highscore = 0 # This variable is used to store the highscore

# This dictionary is used to store the settings and their corresponding values
settings = {
    "max_windows" : 20, # This setting is used to set the maximum number of windows that can be opened at once
    "windows_created_upon_mistake" : 2, # This setting is used to set the number of windows that are created when the user makes a mistake
    "max_window_timer" : 15, # This setting is used to set the maximum time that a window can be open for
    "num_starting_windows" : 1} # This setting is used to set the number of windows that are created when the game starts initially

# Creating the Game window class 
class Game_Window:
    """This class is used to create each game window
    """
    def __init__(self):
        # Create window
        self.root = tk.Tk()
        self.root.title("TIMUS")

        # Finds out users screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Randomizes the size of the window which is to be created
        window_width = random.randint(100, 500)
        window_height = random.randint(100, 350)

        # Figures out where to place the window on the screen so that the window is not off the screen
        xpos = random.randint(0, screen_width - window_width)
        ypos = random.randint(0, screen_height - window_height)

        # Places the window on the screen at this location
        self.root.geometry(f"{window_width}x{window_height}+{xpos}+{ypos}")

        # Disables the resizing of the window
        self.root.resizable(False, False)

        # Forces the game window to be on top of all other currently open windows
        self.root.attributes("-topmost", True)

        # Set window close action to close all currently open windows
        self.root.protocol("WM_DELETE_WINDOW",lambda: Main_Menu.del_windows(Main_Menu))

        # Binds a click on the window to the click() function
        self.root.bind("<Button-1>", self.click)

        # Determines the amount of time to click on the window (random between 4 and 16 seconds)
        self.start_time = time.time()
        self.run_time = random.randint((math.ceil(settings["max_window_timer"]/4)), settings["max_window_timer"])
        self.end_time = self.start_time + self.run_time
        self.time_left = self.end_time - time.time()

        # Creates and places a label which will display the amount of time left
        self.label = tk.Label(self.root, text=str(self.time_left), font=("Trebuchet MS", 50))
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Begins by running the loop() function immediately
        self.loop()

    # Creates a loop function which will run every 100ms for this window
    def loop(self):
        # Updates the amount of time left on the label
        self.time_left = self.end_time - time.time()
        timeleft = round(self.time_left, 1)
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
            for i in range (settings["windows_created_upon_mistake"]):
                Main_Menu.add_window(Main_Menu)
        
        # Runs the loop() function again after 100ms
        self.root.after(100, self.loop)

    # Creates a function which will run every time the user clicks within the window
    def click(self, event):
        global highscore
        if self.time_left < 1: # If the time left is less that 1, run the delete_self() function
            self.delete_self()
            Main_Menu.score+=10
            if Main_Menu.window_count == 0: # If there are no windows left open, add score and return to the main menu 
                if Main_Menu.score > highscore:
                    highscore = Main_Menu.score
                Main_Menu.del_windows(Main_Menu)
                application = Main_Menu()
                
        else: # If the user clicks when the timer is not < 1 second, run the delete_self() function and open 2 more windows
            self.delete_self()
            for i in range (settings["windows_created_upon_mistake"]):
                Main_Menu.add_window(Main_Menu)

    # Create a function which will run when the window is to be deleted
    def delete_self(self):
        self.root.destroy() # Delete the current window
        Main_Menu.window_count -= 1 # Reduce the amount of windows open by 1

# Creating the Instructions window class  
class Instructions:
    """This class is used to create the instructions window
    """
    def __init__(self, action_after):
        global seen_instructions_state
        
        self.action = action_after

        # Create window
        self.root = tk.Tk()
        self.root.title("TIMUS")

        # Sets the size of the window to 600 by 400 pixels
        self.root.geometry("600x400")
        
        # Sets the minimum size that the main menu window can be resized to as 600 by 400 pixels
        self.root.minsize(600, 400)

        # Centers the window
        center(self.root)

        # Creates a frame within the window and grids it
        content = tk.Frame(self.root, padx=12, pady=12, bg="#ff0000")
        content.grid(column=0, row=0, sticky = "nsew")
        
        # Receives the title image from the assets folder and places in on the window
        title_image= tk.PhotoImage(file=get_file_path("instructionstitle.png"))
        title_label = tk.Label(content, image=title_image, bg="#ff0000", padx=5, pady=5)
        title_label.grid(row=0, column=0, columnspan=5, sticky = "nsew", padx=5, pady=5)

        # Creates a label which will display the instructions
        instructions_blurb_image= tk.PhotoImage(file=get_file_path("instructionsblurb.png"))
        instructions_blurb_label = tk.Label(content, borderwidth=10, background="white", relief="groove", image=instructions_blurb_image)
        instructions_blurb_label.grid(row=1, column=2, sticky = "nsew", padx=5, pady=5)

        # Creates a button which will return to the main menu window or start the game depending if the user has read the instructions 
        done_image = tk.PhotoImage(file=get_file_path("done.png"))
        back_button = tk.Button(content, borderwidth=10, background="white", relief="groove", image=done_image)
        if self.action == "start":
            back_button.config(command=lambda: self.start_game(self))
        elif self.action == "mainmenu":
            back_button.config(command=lambda: self.return_to_main_menu(self))
        back_button.grid(row=2, column=2, sticky = "nsew", padx=5, pady=5)

        # Set window close action to return to main menu rather than close the program
        self.root.protocol("WM_DELETE_WINDOW",lambda: self.return_to_main_menu(self))

        # Sets the seeninstructions variable to true
        seen_instructions_state = True

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
        application = Main_Menu()
    
    def start_game(self, event):
        self.root.destroy()
        for i in range(0, settings["num_starting_windows"]):
            Main_Menu.add_window(Main_Menu)

# Creating the Settings window class  
class Settings:
    """This class is used to create the Settings window
    """
    def __init__(self):
        # Create window
        self.root = tk.Tk()
        self.root.title("TIMUS")

        # Sets the size of the window to 600 by 600 pixels
        self.root.geometry("600x500")
        
        # Sets the minimum size that the settings window can be resized to as 600 by 600 pixels
        self.root.minsize(600, 500)

        # Centers the window
        center(self.root)

        # Creates a frame within the window and grids it
        content = tk.Frame(self.root, padx=12, pady=12, bg="#ff0000")
        content.grid(column=0, row=0, sticky = "nsew")
        
        # Receives the title image from the assets folder and places in on the window
        title_image= tk.PhotoImage(file=get_file_path("settingstitle.png"))
        title_label = tk.Label(content, image=title_image, bg="#ff0000", padx=5, pady=5)
        title_label.grid(row=0, column=0, columnspan=4, sticky = "nsew", padx=5, pady=5)

        # Creates a list of settings which are to be created
        setting_labels = ["maxopenwindows", "createduponmistake", "maxtimer", "numstartingwindows"]
        
        # Creates a list of images and spinboxes are to be used for the settings
        images = []
        self.spinboxes = []

        # For each button in the list of buttons, do the following
        for index, setting_labels in enumerate(setting_labels):
            # Add the appropriate image to the list of images so that the image is stored in memory
            images.append(tk.PhotoImage(file=get_file_path(setting_labels + ".png")))
            
            # Create a label for the setting
            setting_label = tk.Label(content, borderwidth=10, background="white", relief="groove", image=images[index])

            # Places the label
            setting_label.grid(row=index+1, column=0, columnspan=2, sticky = "nsew", padx=5, pady=5)
            setting_spinbox = tk.Spinbox(content, from_=1, to=9999, width=3, wrap=True, font=("Trebuchet MS bold", 20), borderwidth=10, background="white", relief="groove", validate= "key")

            # Creates a variable which will store the value of the current setting
            setting_value = tk.IntVar()

            if index == 0: # If the current setting is the max open windows setting
                setting_value.set(settings["max_windows"]) # Set the value of the setting to the current max open windows setting
                setting_spinbox.config(to=50) # Set the maximum value of the spinbox to 50
            elif index == 1: # If the current setting is the created upon mistake setting
                setting_value.set(settings["windows_created_upon_mistake"]) # Set the value of the setting to the current created upon mistake setting
                setting_spinbox.config(to=10) # Set the maximum value of the spinbox to 50
            elif index == 2: # If the current setting is the max timer setting
                setting_value.set(settings["max_window_timer"]) # Set the value of the setting to the current max timer setting
                setting_spinbox.config(from_=4, to=9999) # Set the maximum value of the spinbox to 9999 and the minimum to 4
            elif index == 3: # If the current setting is the max timer setting
                setting_value.set(settings["num_starting_windows"]) # Set the value of the setting to the current max timer setting
                setting_spinbox.config(to=20) # Set the maximum value of the spinbox to 20

            # Configure the default value of the spinbox to the value (determined above)
            setting_spinbox.config(textvariable=setting_value)

            # Sets the validate command to testVal (see below)
            setting_spinbox["validatecommand"] = (setting_spinbox.register(self.testVal),"%P","%d")
            
            # Adds the spinbox to the list of spinboxes
            self.spinboxes.append(setting_spinbox)
            
            # Places the spinbox in the window
            setting_spinbox.grid(row=index+1, column=3, sticky = "nsew", padx=5, pady=5)

        # Creates a button which will reset all settings to default
        set_to_default_image= tk.PhotoImage(file=get_file_path("settodefault.png"))
        set_to_default_button = tk.Button(content, borderwidth=10, background="white", relief="groove", image=set_to_default_image, command=lambda: self.reset_to_default())
        set_to_default_button.grid(row=5, column=0, columnspan=4, sticky = "nsew", padx=5, pady=5)

        # Creates a button which will return to the main menu window 
        done_image = tk.PhotoImage(file=get_file_path("done.png"))
        back_button = tk.Button(content, borderwidth=10, background="white", relief="groove", image=done_image, command=lambda: self.return_to_main_menu())
        back_button.grid(row=6, column=0, columnspan=4, sticky = "nsew", padx=5, pady=5)

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
    
    def testVal(self, character_added, action):
        if action == "1": # If the action is insert character
            if not character_added.isdigit(): # If the character is not a digit
                return False # Return false and allow character to be typed
        return True # Return true and allow character to be typed

    def reset_to_default(self):
        # Calls all global setting variables and resets them to default 
        global settings

        settings = {
            "max_windows" : 20, 
            "windows_created_upon_mistake" : 2,
            "max_window_timer" : 15, 
            "num_starting_windows" : 1}

        # Closes and reopens the settings window
        self.root.destroy()
        application.settings = Settings()

    # Creates a function which is to be run when the user clicks the back button from clicking on the instructions
    def return_to_main_menu(self):
        # Calls all global settings variables
        global settings

        things_changed = False # Creates a variable which will be used to determine if any settings have been changed due to restrictions

        if int(self.spinboxes[0].get()) < 1: # If the max open windows setting is less than 1
            settings["max_windows"] = 1 # Set the max open windows setting to 1
            things_changed = True # Set thingschanged to true
        elif int(self.spinboxes[0].get()) > 50: # If the max open windows setting is greater than 50
            settings["max_windows"] = 50 # Set the max open windows setting to 50
            things_changed = True # Set thingschanged to true
        else:
            settings["max_windows"] = int(self.spinboxes[0].get())
        
        if int(self.spinboxes[1].get()) < 1: # If the created upon mistake setting is less than 1
            settings["windows_created_upon_mistake"] = 1 # Set the created upon mistake setting to 1
            things_changed = True # Set thingschanged to true
        elif int(self.spinboxes[1].get()) > 10: # If the created upon mistake setting is greater than 10
            settings["windows_created_upon_mistake"] = 10 # Set the created upon mistake setting to 10
            things_changed = True # Set thingschanged to true
        else:
            settings["windows_created_upon_mistake"] = int(self.spinboxes[1].get()) 

        if int(self.spinboxes[2].get()) < 4: # If the max timer setting is less than 4
            settings["max_window_timer"] = 4 # Set the max timer setting to 4
            things_changed = True # Set thingschanged to true
        if int(self.spinboxes[2].get()) > 9999: # If the max timer setting is greater than 99999
            settings["max_window_timer"] = 9999 # Set the max timer setting to 9999
            things_changed = True # Set thingschanged to true
        else:
            settings["max_window_timer"] = int(self.spinboxes[2].get())

        if int(self.spinboxes[3].get()) < 1: # If the number of starting windows setting is less than 1
            settings["num_starting_windows"] = 1 # Set the number of starting windows setting to 1
            things_changed = True # Set thingschanged to true
        if int(self.spinboxes[3].get()) > 20: # If the number of starting windows setting is greater than 20
            settings["num_starting_windows"] = 20 # Set the number of starting windows setting to 20
            things_changed = True # Set thingschanged to true
        else:
            settings["num_starting_windows"] = int(self.spinboxes[3].get())
        
        if not things_changed: # If any no settings have been changed due to restrictions 
            # Closes the settings window and opens the main menu window
            self.root.destroy()
            application = Main_Menu()
        else: # If any settings have been changed due to restrictions
            # Closes the settings window and opens the settings window again
            self.root.destroy()
            application.settings = Settings()

# Creating the Main Menu class
class Main_Menu:
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

        # Centers the window
        center(self.root)

        # Creates a frame within the window and grids it
        content = tk.Frame(self.root, padx=12, pady=12, bg="#ff0000")
        content.grid(column=0, row=0, sticky = "nsew")
        
        # Receives the title image from the assets folder and places in on the window
        title_image= tk.PhotoImage(file=get_file_path("title.png"))
        title_label = tk.Label(content, image=title_image, bg="#ff0000")
        title_label.grid(row=0, column=0, rowspan=2, columnspan=5, sticky = "nsew")

        # Creates a label underneath the title which will display the user"s high score
        score_text = "High Score: " + str(highscore)
        score_label = tk.Label(content, borderwidth=10, background="white", relief="groove", text=score_text, font=("Trebuchet MS bold", 12))
        score_label.grid(row=2, column=2, sticky = "nsew", padx=5, pady=5)

        # Creates a list of buttons which are to be created
        button_labels = ["start", "instructions", "settings", "quit"]
        
        # Creates a list of images which are to be used for the buttons
        images = []

        # For each button in the list of buttons, do the following
        for index, button_label in enumerate(button_labels):
            # Add the appropriate image to the list of images so that the image is stored in memory
            images.append(tk.PhotoImage(file=get_file_path(button_label + ".png")))
            
            # Create a button with this image
            button = tk.Button(content, borderwidth=10, background="white", relief="groove", image=images[index])
        
            # Configures the command on the button to run the appropriate function
            if button_label == "start": # If the button is the start button, set the command to run the start() function
                button.config(command=lambda: self.start())
            elif button_label == "instructions":# If the button is the instructions button, set the command to run the instructions() function
                button.config(command=lambda: self.instructions("mainmenu"))
            elif button_label == "settings": # If the button is the settings button, set the command to run the settings() function
                button.config(command=lambda: self.settings())
            elif button_label == "quit": # If the button is the quit button, set the command to close the main menu
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
        Main_Menu.window_count = 0        

        # Create a list of all windows which are currently open
        Main_Menu.windows = []

        # Permanently loop the main menu window 
        self.root.mainloop()
    
    # Creates a function which will run when the start button is clicked
    def start(self):
        Main_Menu.score = 0
        if seen_instructions_state == True:
            self.root.destroy()
            for i in range(0, settings["num_starting_windows"]):
                self.add_window()
        elif seen_instructions_state == False:
            # start the instructions window and after reading the instructions start the game
            self.instructions("start")

    # Creates a function which will run when the instructions button is clicked
    def instructions(self, after_action):
        self.root.destroy()
        self.instructions = Instructions(after_action)

    # Creates a function which will run when the start button is clicked
    def settings(self):
        self.root.destroy()
        self.settings = Settings()

    # Creates a function which will run when a window is to be added
    def add_window(self):
        if Main_Menu.window_count < settings["max_windows"]:
            # Create a new window by creating a new window instance
            window = Game_Window()
            # Save this Window to the list of windows
            Main_Menu.windows.append(window)
            # Increase the amount of windows open by 1
            Main_Menu.window_count += 1
        else:
            Main_Menu.score-=10

    # Creates a function which will run when all windows are to be deleted
    def del_windows(self):
        # For each windows in the list of windows
        for window in Main_Menu.windows:
            try:
                # Delete that window
                window.root.destroy()
            except:
                continue
        # Open the main menu
        application = Main_Menu()

# Starts the main menu
application = Main_Menu()
