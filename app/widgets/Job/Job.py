from tkinter import *
from tkinter import ttk

from modules import convert, crypto # importing the module
from widgets import CustomText # importing the class

class Job(ttk.Frame):
    def __init__(self, parent, file, order, delete_job, *args, **kwargs):
        '''A template frame for displaying information on a specific job'''
        super().__init__(parent, *args, **kwargs)

        job_file = convert.json_to_dict('data/jobs/{}'.format(file))
        self.item = job_file['Name']
        self.quantity = job_file['Quantity']

        # * Mainframe
        mainframe = ttk.Frame(self)
        mainframe.grid(column=0, row=0)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        mainframe.grid_rowconfigure(13, minsize=20)
        
        # * Label
        name = 'Job #{} -- Producing x{} {}(s)'.format(order + 1, self.quantity, self.item)
        info_label = ttk.Label(mainframe, text=name, font=('Arial', 16))
        info_label.grid(column=0, row=0, sticky=W)

        # * Textbox
        textbox = CustomText(mainframe, width=70, height=10)
        textbox.grid(column=0, row=2, columnspan=70, rowspan=10)
        textbox.insert('1.0', convert.dict_to_text(job_file['Materials Used']))
        textbox['state'] = DISABLED

        # * Button
        delete = ttk.Button(mainframe, text='Delete', command=lambda: delete_job(file))
        delete.grid(column=0, row=12, sticky=E)