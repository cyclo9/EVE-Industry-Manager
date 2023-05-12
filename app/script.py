from tkinter import *
from tkinter import ttk
import os

from modules import File, Crypto
from widgets import H_ScrollableFrame
from tabs import Dashboard, Jobs

root = Tk()

class App:
    def __init__(self, root):
        # * root
        root.title('EVE Industry Manager')

        # Set the window dimensions and center it
        width, height = 569, 600
        x = (root.winfo_screenwidth() - width) // 2
        y = (root.winfo_screenheight() - height) // 2
        root.geometry("{}x{}+{}+{}".format(width, height, x, y))
        # root.resizable(0, 0)

        # * Mainframe
        mainframe = H_ScrollableFrame(root)
        mainframe.grid(column=0, row=0)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # * Notebook
        self.n = ttk.Notebook(mainframe, width=515)
        self.n.grid(column=0, row=0)
        self.n.columnconfigure(0, weight=0)
        self.n.rowconfigure(0, weight=0)

        # * Dashboard
        jobs_tab = Jobs(self.n)
        self.n.add(Dashboard(self.n, jobs_tab.add_job), text='Dashboard')

        # * Jobs Page
        self.n.add(jobs_tab, text='Jobs')

if __name__ == '__main__':
    App(root)
    root.mainloop()