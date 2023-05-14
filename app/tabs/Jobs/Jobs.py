from tkinter import *
from tkinter import ttk
import os

from modules import convert, crypto # importing the module
from widgets import V_ScrollableFrame, Job # importing the class

class Jobs(ttk.Frame):
    '''The Job tab lists out all the active jobs'''
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # * Mainframe
        self.mainframe = V_ScrollableFrame(self, width=500, height=500)
        self.mainframe.grid(column=0, row=0, sticky='nwes')
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.scrollable_frame.columnconfigure(0, weight=1)
        self.mainframe.scrollable_frame.rowconfigure(0, weight=1)

        self.load_jobs()

    def delete_children(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def load_jobs(self):
        self.delete_children(self.mainframe.scrollable_frame)
        
        dir = os.listdir('data/jobs')
        for i, file in enumerate(dir):
            Job(self.mainframe.scrollable_frame, file, i, self.delete_job).grid(column=0, row=i)

    def add_job(self, info):
        with open('data/jobs/{}.json'.format(crypto.generate_id()), 'w+') as file:
            file.write(convert.dict_to_json(info))
        self.load_jobs()
    
    def delete_job(self, file):
        os.remove('data/jobs/{}'.format(file))
        self.load_jobs()