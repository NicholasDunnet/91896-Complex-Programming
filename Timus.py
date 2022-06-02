# Importing modules
import tkinter as tk
import pathlib
import os
import random
import time
import math
import pickle

# Creating global functions


def get_file_path(filename):
    """This function returns the filepath of the given filename

    Args:
        filename (string): the name of the file (e.g. "image.png")

    Returns:
        string: the filepath of the given filename (e.g. "C:/Users/User/Desktop/image.png")
    """
    # This gets the current directory where the program is running
    current_dir = pathlib.Path(__file__).parent.resolve()

    # Joins this filepath with the assets folder
    current_dir = os.path.join(current_dir, "assets/")

    # Joins this filepath with the filename
    img_path = os.path.join(current_dir, filename)

    # Returns the complete filepath
    return img_path


def settings_to_default():
    """ This function resets all of the settings to their default values
    """
    # References the global setting dictionary
    global settings

    # Overwrites the current settings dictionary with the default settings
    settings = {
        "max_windows":
        {"value": 20,
         "min": 1,
         "max": 50},
        "windows_created_upon_mistake":
        {"value": 2,
         "min": 1,
         "max": 10},
        "max_window_timer":
        {"value": 15,
         "min": 4,
         "max": 9999},
        "num_starting_windows":
        {"value": 1,
         "min": 1,
         "max": 20}}


def configure_grid(self, content):
    """ This function configures the rows and columns of a grid for resizing

    Args:
        self (object): The window
        content (object): The frame within the window chich within the grid to be configured sits
    """
    # Configures the main window for resizing
    self.root.columnconfigure(0, weight=1)
    self.root.rowconfigure(0, weight=1)

    # Configures the rows and columns within the grid for resizing
    for i in range(0, content.grid_size()[0]):
        content.columnconfigure(i, weight=1)
    for i in range(0, content.grid_size()[1]):
        content.rowconfigure(i, weight=1)

    # Returns
    return


def load_data():
    """ This function loads all saved data, including the settings and the highscore
    """
    # References the global setting dictionary
    global settings

    # References the global highscore
    global highscore

    # If there is a save file, load the settings and score from the save file
    try:
        # Open the file timus.data
        with (open("timus.data", 'rb')) as save:
            data = pickle.load(save)
            highscore = data["highscore"]
            settings = data["settings"]

    # If there is no save file,
    except FileNotFoundError:
        highscore = 0
        settings_to_default()


def save_data():
    """ This function creates a save file of the data at the end of the program
    """
    # Open or create a file called timus.data
    with (open("timus.data", 'wb')) as save:
        # Saves settings and highscore to the save file using pickle
        pickle.dump({"settings": settings, "highscore": highscore}, save)

# Creating global variables


# This variable is used to check if the instructions have been seen since the program has run (by default is false)
seen_instructions_state = False

# This variable is later used to store the highscore (by default is 0)
highscore = 0

# This dictionary is used to store the settings and their corresponding values, minimums and maximums
settings = {}

# Runs the load data function
load_data()

# Creating the a Standard window class


class Standard_Window:
    """ This class contains formatting for a basic window and buttons/labels
    """

    def __init__(self, width, height, minwidth, minheight):
        """ Initilise a new blank window

        Args:
            width (integer): The width of the window
            height (integer): The height of the window
            minwidth (integer): The minimum width the window can be resized to
            minheight (integer): The minimum height the window can be resized to
        """
        # Create window
        self.root = tk.Tk()

        # Set the title of the window to "TIMUS"
        self.root.title("TIMUS")

        # Set the geometery of the window to that which is specified
        self.root.geometry(f"{width}x{height}")

        # Set the minimum size of the window to that which is specified
        self.root.minsize(minwidth, minheight)

        # Forces the window to be on top of all other currently open windows
        self.root.attributes("-topmost", True)

        # Updates the current information on the window so that it can be centered later
        self.root.update_idletasks()

        # Gets the actual width of the window (frame included)
        width = self.root.winfo_width()
        frm_width = self.root.winfo_rootx() - self.root.winfo_x()
        win_width = width + 2 * frm_width

        # Gets the actual height of the window (titlebar included)
        height = self.root.winfo_height()
        titlebar_height = self.root.winfo_rooty() - self.root.winfo_y()
        win_height = height + titlebar_height + frm_width

        # Creates the x and y values of the window
        x = self.root.winfo_screenwidth() // 2 - win_width // 2
        y = self.root.winfo_screenheight() // 2 - win_height // 2

        # Places the window using these x and y values
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        # Stops the window flashing in the wrong location before being moved to center
        self.root.deiconify()

    def button(parent, **kwargs):
        """ Creates a button with default formatting options

        Args:
            parent (object): Where the button is being placed (i.e. frame, canvas)

        Returns:
            tkinter button: A button with the default settings 
        """
        # Retuns a button with default settings of borderwidth, background and relief
        return tk.Button(parent, borderwidth=10, background="white", relief="groove", **kwargs)

    def title_label(parent, **kwargs):
        """ Creates a title label with default formatting options

        Args:
            parent (object): Where the label is being placed (i.e. frame, canvas)

        Returns:
            tkinter label: A label with the default settings 
        """
        # Returns a title label with default settings of background
        return tk.Label(parent, bg="#ff0000", **kwargs)

    def standard_label(parent, **kwargs):
        """ Creates a standard label with default formatting options

        Args:
            parent (object): Where the label is being placed (i.e. frame, canvas)

        Returns:
            tkinter label: A label with the default settings 
        """
        # Returns a title label with default settings of background, borderwidth and relief
        return tk.Label(parent, borderwidth=10, background="white", relief="groove", **kwargs)

# Creating the Game window class


class Game_Window:
    """ This class is used to create each game window
    """

    def __init__(self):
        """ Initialises a new game window
        """
        # Create window
        self.root = tk.Tk()
        self.root.title("TIMUS")

        # Randomizes the size of the window which is to be created
        window_width = random.randint(100, 500)
        window_height = random.randint(100, 350)

        # Finds out users screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Figures out where to place the window on the screen so that the window is not off the screen
        xpos = random.randint(0, screen_width - window_width)
        ypos = random.randint(0, screen_height - window_height)

        # Creates the window on the screen at this location
        self.root.geometry(f"{window_width}x{window_height}+{xpos}+{ypos}")

        # Disables the resizing of the window
        self.root.resizable(False, False)

        # Forces the game window to be on top of all other currently open windows
        self.root.attributes("-topmost", True)

        # Set window close action to close all currently open windows
        self.root.protocol("WM_DELETE_WINDOW",
                           lambda: Main_Menu.del_windows(Main_Menu))

        # Binds a click on the window to the click() function
        self.root.bind(" < Button-1 > ", self.click)

        # Determines the amount of time to click on the window (determined by the current settings)
        self.start_time = time.time()
        self.run_time = random.randint((math.ceil(
            settings["max_window_timer"]["value"]/4)), settings["max_window_timer"]["value"])
        self.end_time = self.start_time + self.run_time
        self.time_left = self.end_time - time.time()

        # Creates and places a label which will display the amount of time left
        self.label = tk.Label(self.root, text=str(
            self.time_left), font=("Trebuchet MS", 50))
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Begins by running the loop() function immediately
        self.loop()

    def loop(self):
        """ This function runs every 100ms for each game window
        """
        # Updates the amount of time left on the label
        self.time_left = self.end_time - time.time()
        timeleft = round(self.time_left, 1)
        self.label.config(text=str(timeleft))

        # If the time left is greater than 5, set background of window and label to green
        if timeleft > 5:
            self.label.config(bg="green")
            self.root.config(bg="green")
        # If the time left is greater than 3, set background of window and label to yellow
        elif timeleft > 3:
            self.label.config(bg="yellow")
            self.root.config(bg="yellow")
        # If the time left is greater than 1, set background of window and label to red
        elif timeleft > 1:
            self.label.config(bg="red")
            self.root.config(bg="red")
        # If the time left is greater than 0, set background of window and label to black and the text color to white
        elif timeleft > 0:
            self.label.config(bg="black", fg="white")
            self.root.config(bg="black")
        # If the time left is less than 0 (if the user does not click on the window in time);
        else:
            # Run the delete self function
            self.delete_self()
            # Open the correct amount of game windows (determined by the current setting)
            for i in range(settings["windows_created_upon_mistake"]["value"]):
                Main_Menu.add_window(Main_Menu)

        # Runs the loop() function again after 100ms
        self.root.after(100, self.loop)

    def click(self, event):
        """ This function processes a click on any open game window

        Args:
            event (object): The event that happened (i.e. left mouse click)
        """
        # References the global high score variable
        global highscore

        # If the time left is less that 1
        if self.time_left < 1:
            # Run the delete self function
            self.delete_self()

            # Add 10 points to the users current score
            Main_Menu.score += 10

            # If there are no windows left open
            if Main_Menu.window_count == 0:
                # If the users current score is greater than the high score
                if Main_Menu.score > highscore:
                    # Set the high score to the users current score
                    highscore = Main_Menu.score

                # Delete the data from all of the windows
                Main_Menu.del_windows(Main_Menu)

                # Open the Main Menu
                application = Main_Menu()

        else:  # If the user clicks when the timer is not < 1 second, run the delete_self() function and open 2 more windows
            self.delete_self()
            for i in range(settings["windows_created_upon_mistake"]["value"]):
                Main_Menu.add_window(Main_Menu)

    def delete_self(self):
        """ This function will delete the given window
        """
        # Delete the current window
        self.root.destroy()

        # Reduce the amount of windows open by 1
        Main_Menu.window_count -= 1

# Creating the Instructions window class


class Instructions:
    """ This class is used to create the instructions window
    """

    def __init__(self, action_after):
        """ Initialises the instructions window

        Args:
            action_after (string): The action which is to be performed after the instructions window closes
        """
        # References the seen instructions state
        global seen_instructions_state

        # Stores the action to perform afterwards to self.action
        self.action = action_after

        # Creates a standard window
        Standard_Window.__init__(self, 900, 700, 900, 700)

        # Creates a frame within the window and grids it
        content = tk.Frame(self.root, padx=12, pady=12, bg="#ff0000")
        content.grid(column=0, row=0, sticky="nsew")

        # Receives the title image from the assets folder and places in on the window
        title_image = tk.PhotoImage(
            file=get_file_path("instructionstitle.png"))
        title_label = Standard_Window.title_label(content, image=title_image)
        title_label.grid(row=0, column=0, columnspan=5,
                         sticky="nsew", padx=5, pady=5)

        # Creates a label which will display the instructions
        instructions_blurb_image = tk.PhotoImage(
            file=get_file_path("instructionsblurb.png"))
        instructions_blurb_label = Standard_Window.standard_label(
            content, image=instructions_blurb_image)
        instructions_blurb_label.grid(
            row=1, column=2, sticky="nsew", padx=5, pady=5)

        # Creates a button which will perform an action after the user has read the instructions
        done_image = tk.PhotoImage(file=get_file_path("done.png"))
        back_button = Standard_Window.button(content, image=done_image)

        # If the action to perform afterwards is to start the game
        if self.action == "start":
            # Configure the button to run the start game function in the main menu class
            back_button.config(command=lambda: Main_Menu.start_game(self))

        # If the action to perform afterwars is to return to the main menu
        elif self.action == "mainmenu":
            # Configure the button to run the return to main menu function in the main menu class
            back_button.config(
                command=lambda: Main_Menu.return_to_main_menu(self))

        # Place the back button in the window
        back_button.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        # Set window close action to return to main menu rather than close the program
        self.root.protocol("WM_DELETE_WINDOW",
                           lambda: Main_Menu.return_to_main_menu(self))

        # Sets the seeninstructions variable to true
        seen_instructions_state = True

        # Configure all columns and rows within the instructions window to expand to fill the window if resized
        configure_grid(self, content)

        # Loops the window
        self.root.mainloop()

# Creating the Settings window class


class Settings:
    """ This class is used to create the Settings window
    """

    def __init__(self):
        """ Initialises the settings window
        """
        # Creates a standard window
        Standard_Window.__init__(self, 600, 500, 600, 500)

        # Creates a frame within the window and grids it
        content = tk.Frame(self.root, padx=12, pady=12, bg="#ff0000")
        content.grid(column=0, row=0, sticky="nsew")

        # Receives the title image from the assets folder and places in on the window
        title_image = tk.PhotoImage(file=get_file_path("settingstitle.png"))
        title_label = Standard_Window.title_label(content, image=title_image)
        title_label.grid(row=0, column=0, columnspan=4,
                         sticky="nsew", padx=5, pady=5)

        # Creates a list of images and spinboxes are to be used for the settings
        images = []
        self.spinboxes = []

        # For each button in the list of buttons, do the following
        for index, setting in enumerate(settings.items()):
            # Add the appropriate image to the list of images so that the image is stored in memory
            images.append(tk.PhotoImage(
                file=get_file_path(setting[0] + ".png")))

            # Create a label for the setting
            setting_label = Standard_Window.standard_label(
                content, image=images[index])

            # Places the label
            setting_label.grid(row=index+1, column=0,
                               columnspan=2, sticky="nsew", padx=5, pady=5)
            setting_spinbox = tk.Spinbox(content, from_=setting[1]["min"], to=setting[1]["max"], width=3, wrap=True, font=(
                "Trebuchet MS bold", 20), borderwidth=10, background="white", relief="groove", validate="key")

            # Creates a variable which will store the value of the current setting
            setting_value = tk.IntVar()
            setting_value.set(setting[1]["value"])
            setting_spinbox.config(textvariable=setting_value)

            # Sets the validate command to testVal (see below)
            setting_spinbox["validatecommand"] = (
                setting_spinbox.register(self.test_value), "%P", "%d")

            # Adds the spinbox to the list of spinboxes
            self.spinboxes.append(setting_spinbox)

            # Places the spinbox in the window
            setting_spinbox.grid(row=index+1, column=3,
                                 sticky="nsew", padx=5, pady=5)

        # Creates a button which will reset all settings to default
        set_to_default_image = tk.PhotoImage(
            file=get_file_path("settodefault.png"))
        set_to_default_button = Standard_Window.button(
            content, image=set_to_default_image, command=lambda: self.reset_to_default())
        set_to_default_button.grid(
            row=5, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        # Creates a button which will return to the main menu window
        done_image = tk.PhotoImage(file=get_file_path("done.png"))
        back_button = tk.Button(content, borderwidth=10, background="white", relief="groove",
                                image=done_image, command=lambda: self.return_to_main_menu())
        back_button.grid(row=6, column=0, columnspan=4,
                         sticky="nsew", padx=5, pady=5)

        # Set window close action to return to main menu rather than close the program
        self.root.protocol("WM_DELETE_WINDOW",
                           lambda: Main_Menu.return_to_main_menu(self))

        # Configures the settings grid so that resizing the window works appropriately
        configure_grid(self, content)

        # Loops the Settings menu
        self.root.mainloop()

    def test_value(self, character_added, action):
        """ This function is used to check if a character added to a spinbox is a valid intiger

        Args:
            character_added (string): What character is being added
            action (string): What type of action is being performed

        Returns:
            boolean: Whether the character is allowed to be added or not
        """
        # If the action is insert character
        if action == "1":
            # If the character is not a digit
            if not character_added.isdigit():
                # Return false and dont allow character to be typed
                return False
        # Return true and allow character to be typed
        return True

    def reset_to_default(self):
        """ This function is used to reset all settings to default
        """
        # References the global settings dictionary
        global settings

        # Runs the settings to default function
        settings_to_default()

        # Closes and reopens the settings window
        self.root.destroy()
        application.settings = Settings()

    def return_to_main_menu(self):
        """ This function runs when the user either clicks the back button or closes the window
        """
        # References the global settings dictionary
        global settings

        # Creates a variable which will be used to determine if any settings have been changed due to restrictions
        things_changed = False

        # For each setting in settings
        for index, setting in enumerate(settings.items()):
            # If the value of the spinbox is less than the minimum value of the setting
            if int(self.spinboxes[index].get()) < setting[1]["min"]:
                # Set the value of the setting to the minimum
                setting[1]["value"] = setting[1]["min"]

                # Set the things changed variable to True
                things_changed = True

            # If the value of the spinbox is greater than the maximum value of the setting
            elif int(self.spinboxes[index].get()) > setting[1]["max"]:
                # Set the value of the setting to the maximum
                setting[1]["value"] = setting[1]["max"]

                # Set the things changed variable to True
                things_changed = True
            # If the value of the spinbox is between the maximum and minimum value of the given setting
            else:
                # Set the value of the setting to the value of the spinbox
                setting[1]["value"] = int(self.spinboxes[index].get())

        # If any no settings have been changed due to restrictions
        if not things_changed:
            # Closes the settings window and opens the main menu window
            Main_Menu.return_to_main_menu(self)

        # If any settings have been changed due to restrictions
        else:
            # Closes the settings window and opens the settings window again
            self.root.destroy()
            application.settings = Settings()

# Creating the Main Menu class


class Main_Menu:
    """ This class is used to create the Main Menu window
    """

    def __init__(self):
        """ Initialises the Main Menu window
        """
        # Creates a standard window
        Standard_Window.__init__(self, 600, 400, 300, 400)

        # Creates a frame within the window and grids it
        content = tk.Frame(self.root, padx=12, pady=12, bg="#ff0000")
        content.grid(column=0, row=0, sticky="nsew")

        # Receives the title image from the assets folder and places in on the window
        title_image = tk.PhotoImage(file=get_file_path("title.png"))
        title_label = Standard_Window.title_label(content, image=title_image)
        title_label.grid(row=0, column=0, rowspan=2,
                         columnspan=5, sticky="nsew")

        # Creates a label underneath the title which will display the user"s high score
        score_text = "High Score: " + str(highscore)
        score_label = Standard_Window.standard_label(
            content, text=score_text, font=("Trebuchet MS bold", 12))
        score_label.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        # Creates a list of buttons which are to be created
        button_labels = ["start", "instructions", "settings", "quit"]

        # Creates a list of images which are to be used for the buttons
        images = []

        # For each button in the list of buttons, do the following
        for index, button_label in enumerate(button_labels):
            # Add the appropriate image to the list of images so that the image is stored in memory
            images.append(tk.PhotoImage(
                file=get_file_path(button_label + ".png")))

            # Create a button with this image
            button = Standard_Window.button(content, image=images[index])

            # If the button is the start button, set the command to run the start() function
            if button_label == "start":
                button.config(command=lambda: self.start_check())
            # If the button is the instructions button, set the command to run the instructions() function
            elif button_label == "instructions":
                button.config(command=lambda: self.instructions("mainmenu"))
            # If the button is the settings button, set the command to run the settings() function
            elif button_label == "settings":
                button.config(command=lambda: self.settings())
            # If the button is the quit button, set the command to close the main menu
            elif button_label == "quit":
                button.config(command=lambda: self.end_game())

            # Place the button in descending order in the main menu window
            button.grid(column=2, row=index + 3, sticky="nsew", padx=5, pady=5)

        # Configure all columns and rows within the main menu window to expand to fill the window if resized
        configure_grid(self, content)

        # Creates a variable which will store the amount of windows open
        Main_Menu.window_count = 0

        # Create a list of all windows which are currently open
        Main_Menu.windows = []

        # Permanently loop the main menu window
        self.root.mainloop()

    def start_check(self):
        """ This function will check if the user is able to start the game
        """
        # If the user has seen the instructions
        if seen_instructions_state == True:
            # Run the start game function
            self.start_game()
        # If the user has not seen the instructions
        elif seen_instructions_state == False:
            # Start the instructions window with the after-action to start the game
            self.instructions("start")

    def start_game(self):
        """ This function starts the game
        """
        # Set the current score of the game to 0
        Main_Menu.score = 0
        # CLoses the current window
        self.root.destroy()
        # For a range of 0 to the number of starting windows setting
        for i in range(0, settings["num_starting_windows"]["value"]):
            # Run the add window function
            Main_Menu.add_window(self)

    def add_window(self):
        """ This function will run every time a new game window is to be added
        """
        # If the current window count is less than the maximum windows setting
        if Main_Menu.window_count < settings["max_windows"]["value"]:
            # Create a new window by creating a new window instance
            window = Game_Window()
            # Save this Window to the list of windows
            Main_Menu.windows.append(window)
            # Increase the amount of windows open by 1
            Main_Menu.window_count += 1
        # If the current window count is equal to or greater than the maximum window setting
        else:
            # Remove 10 points from the users score and dont open another window
            Main_Menu.score -= 10

    def del_windows(self):
        """ This function will run when all windows are to be deleted
        """
        # For each windows in the list of windows
        for window in Main_Menu.windows:
            try:
                # Delete that window
                window.root.destroy()
            except:
                continue
        # Open the main menu
        application = Main_Menu()

    def instructions(self, after_action):
        """ This function will run when the instructions are to be opened

        Args:
            after_action (string): The action which is to be performed after the instructions have been read
        """
        # Closes the current window
        self.root.destroy()
        # Opens the instructions window
        self.instructions = Instructions(after_action)

    def settings(self):
        """ This function will run when the settings button is clicked
        """
        # Closes the current window
        self.root.destroy()
        # Opens the settings window
        self.settings = Settings()

    def return_to_main_menu(self):
        """ This function is run when the main menu is to be opened
        """
        # Closes the current window
        self.root.destroy()
        # Opens the main menu
        application = Main_Menu()

    def end_game(self):
        """ This function is run when the game is to be closed
        """
        # Closes the current window
        self.root.destroy()
        # Runs the save data function
        save_data()


# Starts the main menu
application = Main_Menu()
