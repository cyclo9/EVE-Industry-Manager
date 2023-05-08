from tkinter import *
from tkinter import ttk

from frames.manager import Manager

root = Tk()

class App:
    def __init__(self, root):
        # * root
        root.title('EVE Industry Manager')
        # centers window
        w = 550; h = 900
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        root.resizable(0, 0)

        # * mainframe
        mainframe = ttk.Frame(root)
        mainframe.grid(column=0, row=0)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # * Notebook
        n = ttk.Notebook(mainframe)
        n.grid(column=0, row=0)

        # Manager
        n.add(Manager(n), text='Manager')

if __name__ == '__main__':
    App(root)
    root.mainloop()