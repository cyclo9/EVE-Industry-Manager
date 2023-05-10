from tkinter import *
from tkinter import ttk
import re
import json

from widgets import CustomText, ScrollableFrame

class Manager(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # * Mainframe
        mainframe = ScrollableFrame(self, width=500, height=500)
        mainframe.grid(column=0, row=0, sticky='nwes')
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.scrollable_frame.columnconfigure(0, weight=1)
        mainframe.scrollable_frame.rowconfigure(0, weight=1)

        # * Frames
        inv_frm = ttk.Frame(mainframe.scrollable_frame)
        recipe_frm = ttk.Frame(mainframe.scrollable_frame)
        input_frm = ttk.Frame(mainframe.scrollable_frame) # combines both the item and job widgets together for betting aligmment
        mats_req_frm = ttk.Frame(mainframe.scrollable_frame)
        mats_missing_frm = ttk.Frame(mainframe.scrollable_frame)

        inv_frm.grid(column=0, row=0, columnspan=70, sticky=W)
        mainframe.scrollable_frame.grid_rowconfigure(1, minsize=10)
        recipe_frm.grid(column=0, row=2, columnspan=70, sticky=W)
        input_frm.grid(column=0, row=3, columnspan=70)
        input_frm.grid_rowconfigure(1, minsize=10)
        mats_req_frm.grid(column=0, row=4, columnspan=70, sticky=W)

        # * Inventory
        # Label
        inv_label = ttk.Label(inv_frm, text='Inventory')
        inv_label.grid(column=0, row=0)
        # Entrybox
        self.inventory = CustomText(inv_frm, width=70, height=10)
        self.inventory.bind('<<TextInsert>>', self.parse_inventory)
        self.inventory.grid(column=0, row=1, columnspan=70, rowspan=10)

        # * Recipe
        # Label
        recipe_label = ttk.Label(recipe_frm, text='Recipe')
        recipe_label.grid(column=0, row=0)
        # Entrybox
        self.recipe = CustomText(recipe_frm, width=70, height=10)
        self.recipe.grid(column=0, row=1, columnspan=70, rowspan=10)
        # * Item
        # Label
        item_label = ttk.Label(input_frm, text='Item Name:')
        item_label.grid(column=0, row=0)
        # Entry
        self.item = StringVar()
        item_entry = ttk.Entry(input_frm, textvariable=self.item, width=15)
        item_entry.grid(column=1, row=0)
        # Save Button
        save_recipe = ttk.Button(input_frm, text='Save', command=self.save_recipe)
        save_recipe.grid(column=2, row=0)

        # * Job
        # Label
        job_label = ttk.Label(input_frm, text='Start Job:')
        job_label.grid(column=0, row=2)
        # Entry
        job = StringVar()
        job_entry = ttk.Entry(input_frm, textvariable=job, width=15)
        job_entry.grid(column=1, row=2)
        # Start Button
        start_job = ttk.Button(input_frm, text='Start')
        start_job.grid(column=2, row=2)

        # * Materials Required
        # Label
        mats_req_label = ttk.Label(mats_req_frm, text='Materials Required')
        mats_req_label.grid(column=0, row=0)
        # Textbox
        mats_req = CustomText(mats_req_frm, width=70, height=10)
        mats_req.grid(column=0, row=1, columnspan=70, rowspan=70)

    def parse_inventory(self, *args):
        content = self.inventory.get('1.0', 'end').splitlines()
        inventory = {}

        for line in content:
            try:
                array = re.split(r'\t+', line.rstrip('\n'))
                item = array[0]
                quantity = int(array[1].replace(',', ''))
                inventory[item] = quantity
            except:
                pass

        print(json.dumps(inventory, indent=4))

        file = open('data/inventory.json', 'w+')
        file.write(json.dumps(inventory, indent=4))
        file.close

    def save_recipe(self, *args):
        content = self.recipe.get('1.0', 'end').splitlines()
        content.pop(0)
        recipe = {}

        for line in content:
            try:
                array = line.split(' x ')
                item = array[1]
                quantity = int(array[0])
                recipe[item] = quantity
            except:
                pass
        
        if self.item.get() != '': # this prevents saving an empty file
            file = open('data/recipes/{}.json'.format(self.item.get().lower()), 'w+')
            file.write(json.dumps(recipe, indent=4))
            file.close

        self.item.set('')
        self.recipe.delete('1.0', 'end')