from tkinter import *
from tkinter import ttk
import re
import json
import os

from widgets import CustomText, ScrollableFrame

class Manager(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        '''The Manager tab which is in charge taking inventory, saving recipes, and calculating materials required and missing.'''
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
        input_frm.grid_rowconfigure(1, minsize=20)
        mats_req_frm.grid(column=0, row=4, columnspan=70, sticky=W)
        mainframe.scrollable_frame.grid_rowconfigure(5, minsize=10)
        mats_missing_frm.grid(column=0, row=6, columnspan=70)

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
        item_entry = ttk.Entry(input_frm, textvariable=self.item, width=20)
        item_entry.grid(column=1, row=0, columnspan=2, sticky=W)
        # Save Button
        save_recipe = ttk.Button(input_frm, text='Save', command=self.save_recipe)
        save_recipe.grid(column=3, row=0)
        item_entry.bind('<Return>', lambda e: save_recipe.invoke())

        # * Selecting the Item
        # Label
        select_item_label = ttk.Label(input_frm, text='Select Item:')
        select_item_label.grid(column=0, row=2)
        # Entry
        self.selected_item = StringVar()
        select_item_entry = ttk.Entry(input_frm, textvariable=self.selected_item, width=15)
        select_item_entry.grid(column=1, row=2, sticky=EW)
        # Multiplier
        self.multiplier = IntVar(value=1)
        multiplier_entry = ttk.Entry(input_frm, textvariable=self.multiplier, width=3)
        multiplier_entry.grid(column=2, row=2)
        multiplier_entry.bind('<FocusIn>', lambda e: multiplier_entry.select_range(0, END))
        multiplier_entry.bind('<Return>', lambda e: calculate.invoke())
        # Calculate Button
        calculate = ttk.Button(input_frm, text='Calculate', command=self.retrieve_mats)
        calculate.grid(column=3, row=2)
        select_item_entry.bind('<Return>', lambda e: calculate.invoke())

        # * Materials Required
        # Label
        mats_req_label = ttk.Label(mats_req_frm, text='Materials Required')
        mats_req_label.grid(column=0, row=0)
        # Textbox
        self.mats_req = {}
        self.mats_req_textbox = CustomText(mats_req_frm, state=DISABLED, width=70, height=10)
        self.mats_req_textbox.grid(column=0, row=1, columnspan=70, rowspan=70)

        # * Materials Missing
        # Label
        mats_missing_label = ttk.Label(mats_missing_frm, text='Materials Missing')
        mats_missing_label.grid(column=0, row=0)
        # Textbox
        self.mats_missing = {}
        self.mats_missing_textbox = CustomText(mats_missing_frm, state=DISABLED, width=70, height=10)
        self.mats_missing_textbox.grid(column=0, row=1, columnspan=70, rowspan=10)

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

    def calc_mats_req(self, item):
        dir = os.listdir('data/recipes')
        target_file = '{}.json'.format(item.lower())
        for i, file in enumerate(dir): # go through the directory
            if file == target_file: # find the file that matches with one looking for
                current_ingredient = target_file.split('.json')[0].title()
                try:
                    del self.mats_req[current_ingredient]
                except:
                    pass
                selected_file = open('data/recipes/{}'.format(dir[i]), 'r') # open taht file up
                recipe = json.loads(''.join(selected_file.readlines())) # load it into json
                selected_file.close()
                for ingredient in recipe:
                    self.mats_req[ingredient] = recipe[ingredient] * self.multiplier.get() # for each ingredient in the recipe, add it to the masterlist
                    self.calc_mats_req(ingredient) # find the ingredients of each ingredient
    
    def calc_mats_missing(self):
        inventory_file = open('data/inventory.json', 'r')
        inventory = json.loads(''.join(inventory_file.readlines()))
        for ingredient in self.mats_req:
            if ingredient in inventory:
                qty_missing = self.mats_req[ingredient] - inventory[ingredient] 
                if qty_missing > 0:
                    self.mats_missing[ingredient] = qty_missing
            else:
                self.mats_missing[ingredient] = self.mats_req[ingredient]

    def retrieve_mats(self, *args):
        self.calc_mats_req(self.selected_item.get())
        mats_req = []
        for ingredient in self.mats_req:
            mats_req.append('{} {}'.format(self.mats_req[ingredient], ingredient))
        self.mats_req_textbox['state'] = NORMAL
        self.mats_req_textbox.insert('1.0', '\n'.join(mats_req))
        self.mats_req_textbox['state'] = DISABLED

        self.calc_mats_missing()
        mats_missing = []
        for ingredient in self.mats_missing:
            mats_missing.append('{} {}'.format(self.mats_missing[ingredient], ingredient))
        self.mats_missing_textbox['state'] = NORMAL
        self.mats_missing_textbox.insert('1.0', '\n'.join(mats_missing))
        self.mats_missing_textbox['state'] = DISABLED