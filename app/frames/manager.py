from tkinter import *
from tkinter import ttk
import numpy as np
import re
import json

from widgets.CustomText import CustomText

class Manager(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # * Inventory
        # Label
        inv_label = ttk.Label(self, text='Inventory')
        inv_label.grid(column=0, row=0, sticky=(W))

        # Textbox
        inventory = CustomText(self, width=70, height=10)
        inventory.grid(column=0, row=1, columnspan=15)
        inventory.bind('<<TextModified>>', lambda e: self.parse_inventory(inventory.get('1.0', 'end')))

    def parse_inventory(self, text):
        content = text.splitlines()

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
        return