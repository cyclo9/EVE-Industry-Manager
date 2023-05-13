from tkinter import *
from tkinter import ttk
    
class V_ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        '''A custom Frame widget that is scrollable.'''
        super().__init__(container, *args, **kwargs)

        self.canvas = Canvas(self, highlightthickness=0, *args, **kwargs)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox('all')
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky=NSEW)
        scrollbar.grid(row=0, column=1, sticky=NS)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)