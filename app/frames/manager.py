from tkinter import *
from tkinter import ttk
import re
import json

from widgets.CustomText import CustomText

class Manager(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # * Inventory
        # Label
        inv_label = ttk.Label(self, text='Inventory')
        inv_label.grid(column=0, row=0, columnspan=4, sticky=W)
        # Entrybox
        self.inventory = CustomText(self, width=70, height=10)
        self.inventory.bind('<<TextInsert>>', self.parse_inventory)
        self.inventory.grid(column=0, row=1, columnspan=70, rowspan=10, sticky=W)

        ttk.Label(self, text='').grid(column=0, row=12, columnspan=70)

        # * Recipe
        # Label
        recipe_label = ttk.Label(self, text='Recipe')
        recipe_label.grid(column=0, row=13, columnspan=4, sticky=W)
        # Entrybox
        self.recipe = CustomText(self, width=70, height=10)
        self.recipe.grid(column=0, row=14, columnspan=70, rowspan=10)

        # * Item
        # Label
        item_label = ttk.Label(self, text='Item Name:')
        item_label.grid(column=0, row=25, columnspan=4, sticky=W)
        # Entry
        self.item = StringVar()
        item_entry = ttk.Entry(self, textvariable=self.item, width=15)
        item_entry.grid(column=5, row=25, columnspan=15, sticky=W)
        # Save Button
        save_recipe = ttk.Button(self, text='Save', command=self.save_recipe)
        save_recipe.grid(column=21, row=25, columnspan=10, sticky='w')

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
        
        file = open('data/recipes/{}.json'.format(self.item.get()), 'w+')
        file.write(json.dumps(recipe, indent=4))
        file.close

        self.item.set('')
        self.recipe.delete('1.0', 'end')