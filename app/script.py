from tkinter import *
from tkinter import ttk

from widgets import H_ScrollableFrame
from tabs import Manager, Job

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

        # * Manager
        self.n.add(Manager(self.n), text='Manager')

        ttk.Button(mainframe, text='Add Tab', command=lambda: self.add_tab('New Tab')).grid(column=0, row=1)

    def add_tab(self, tab_name: str):
        test = Job(self.n, self.delete_tab, tab_name)
        self.n.add(test, text=tab_name)

    def delete_tab(self, tab_name):
        for tab in self.n.tabs():
            if self.n.tab(tab, "text") == tab_name:
                self.n.forget(tab)
                break

if __name__ == '__main__':
    App(root)
    root.mainloop()