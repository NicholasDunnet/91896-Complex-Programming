# importing modules
import tkinter as tk

# setting up window
root = tk.Tk()
root.title('TIMUS')
root.geometry('600x400')

content = tk.Frame(root, padx=12, pady=12, bg='#ff0000')
content.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

titlelabel = tk.Label(content, text='Timus', bg='#ff0000')
titlelabel.grid(row=0, column=0, rowspan=2, columnspan=5, sticky=tk.N+tk.S+tk.E+tk.W)

startbutton = tk.Button(content, borderwidth = 10, background = 'white', relief = 'groove', text='Start', height=1, command=lambda: root.destroy())
startbutton.grid(row=2, column=2, rowspan=1, columnspan= 1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

instructionsbutton = tk.Button(content, borderwidth = 10, background = 'white', relief = 'groove', text='Instructions', height=1, command=lambda: root.destroy())
instructionsbutton.grid(row=3, column=2, rowspan=1, columnspan= 1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

settingsbutton = tk.Button(content, borderwidth = 10, background = 'white', relief = 'groove', text='Settings', height=1, command=lambda: root.destroy())
settingsbutton.grid(row=4, column=2, rowspan=1, columnspan= 1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

quitbutton = tk.Button(content, borderwidth = 10, background = 'white', relief = 'groove', text='Quit', height=1, command=lambda: root.destroy())
quitbutton.grid(row=5, column=2, rowspan=1, columnspan= 1, sticky=tk.N+tk.S+tk.E+tk.W, padx=5, pady=5)

# loop the window
root.mainloop()