from tkinter import *
from tkinter import ttk

from frames.manager import Manager

root = Tk()

class App:
    def __init__(self, root):
        # * root
        root.title('EVE Industry Manager')

        # Set the window dimensions and center it
        width, height = 550, 550
        x = (root.winfo_screenwidth() - width) // 2
        y = (root.winfo_screenheight() - height) // 2
        root.geometry("{}x{}+{}+{}".format(width, height, x, y))
        # root.resizable(0, 0)

        # * mainframe
        mainframe = ttk.Frame(root)
        mainframe.grid(column=0, row=0)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # * Notebook
        n = ttk.Notebook(mainframe)
        n.grid(column=0, row=0)
        n.columnconfigure(0, weight=1)
        n.rowconfigure(0, weight=1)

        # Manager
        n.add(Manager(n), text='Manager')

if __name__ == '__main__':
    App(root)
    root.mainloop()