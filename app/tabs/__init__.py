from tkinter import *
from tkinter import ttk
import re
import os

from modules import File, Crypto
from widgets import CustomText, V_ScrollableFrame

class Dashboard(ttk.Frame):
    def __init__(self, parent, add_job, *args, **kwargs):
        '''The Dashboard tab is in charge taking inventory, saving recipes, calculating materials required and missing, and starting jobs.'''
        super().__init__(parent, *args, **kwargs)
        self.add_job = add_job

        # * Mainframe
        mainframe = V_ScrollableFrame(self, width=500, height=500)
        mainframe.grid(column=0, row=0, sticky='nwes')
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.scrollable_frame.columnconfigure(0, weight=1)
        mainframe.scrollable_frame.rowconfigure(0, weight=1)

        mainframe.scrollable_frame.grid_rowconfigure(1, minsize=10)
        mainframe.scrollable_frame.grid_rowconfigure(5, minsize=10)
        mainframe.scrollable_frame.grid_rowconfigure(7, minsize=10)

        # * Frames
        inv_frm = ttk.Frame(mainframe.scrollable_frame)
        inv_frm.grid(column=0, row=0, columnspan=70, sticky=W)

        recipe_frm = ttk.Frame(mainframe.scrollable_frame)
        recipe_frm.grid(column=0, row=2, columnspan=70, sticky=W)

        # combines both the item and job widgets together for betting aligmment
        input_frm = ttk.Frame(mainframe.scrollable_frame) 
        input_frm.grid(column=0, row=3, columnspan=70)
        input_frm.grid_rowconfigure(1, minsize=20)

        mats_req_frm = ttk.Frame(mainframe.scrollable_frame)
        mats_req_frm.grid(column=0, row=4, columnspan=70, sticky=W)
        
        mats_missing_frm = ttk.Frame(mainframe.scrollable_frame)
        mats_missing_frm.grid(column=0, row=6, columnspan=70)

        jobs_frm = ttk.Frame(mainframe.scrollable_frame)
        jobs_frm.grid(column=0, row=8, columnspan=70)

        # * Inventory
        # Label
        inv_label = ttk.Label(inv_frm, text='Inventory')
        inv_label.grid(column=0, row=0)
        # Entrybox
        self.inventory = CustomText(inv_frm, width=70, height=10)
        self.inventory.bind('<<TextInsert>>', self.save_inventory)
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
        # Calculate Button
        calculate = ttk.Button(input_frm, text='Calculate', command=self.retrieve_mats)
        calculate.grid(column=3, row=2)
        select_item_entry.bind('<Return>', lambda e: calculate.invoke())
        multiplier_entry.bind('<Return>', lambda e: calculate.invoke())

        # * Materials Required
        # Label
        self.mats_req = {}
        mats_req_label = ttk.Label(mats_req_frm, text='Materials Required')
        mats_req_label.grid(column=0, row=0)
        # Textbox
        self.mats_req_textbox = CustomText(mats_req_frm, state=DISABLED, width=70, height=10)
        self.mats_req_textbox.grid(column=0, row=1, columnspan=70, rowspan=70)

        # * Materials Missing
        # Label
        mats_missing_label = ttk.Label(mats_missing_frm, text='Materials Missing')
        mats_missing_label.grid(column=0, row=0)
        # Textbox
        self.mats_missing_textbox = CustomText(mats_missing_frm, state=DISABLED, width=70, height=10)
        self.mats_missing_textbox.grid(column=0, row=1, columnspan=70, rowspan=10)

        # * Starting Jobs
        # Label
        job_label = ttk.Label(jobs_frm, text='Job:')
        job_label.grid(column=0, row=0)
        # Entry
        self.job = StringVar()
        job_entry = ttk.Entry(jobs_frm, textvariable=self.job, width=15)
        job_entry.grid(column=1, row=0, sticky=EW)
        # Multiplier
        self.quantity = IntVar(value=1)
        quantity_entry = ttk.Entry(jobs_frm, textvariable=self.quantity, width=3)
        quantity_entry.grid(column=2, row=0)
        quantity_entry.bind('<FocusIn>', lambda e: quantity_entry.select_range(0, END))
        # Button
        start_job_button = ttk.Button(jobs_frm, text='Start Job', command=self.start_job)
        start_job_button.grid(column=3, row=0)
        job_entry.bind('<Return>', lambda e: start_job_button.invoke())
        quantity_entry.bind('<Return>', lambda e: start_job_button.invoke())

    def save_inventory(self):
        '''Saves list of items into an inventory file.'''
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
        file.write(File().dict_to_json(inventory))
        file.close

    def save_recipe(self):
        '''Saves the blueprint recipe for an item.'''
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
            file.write(File().dict_to_json(recipe))
            file.close

        self.item.set('')
        self.recipe.delete('1.0', 'end')

    def calc_mats_req(self, item: str, multiplier):
        '''Calculates the materials required to manufacture the selected item.'''
        dir = os.listdir('data/recipes')
        target_file = '{}.json'.format(item.lower())
        for i, file in enumerate(dir):
            if file == target_file:
                current_ingredient = target_file.split('.json')[0].title()
                try:
                    del self.mats_req[current_ingredient]
                except:
                    pass
                recipe = File().json_to_dict('data/recipes/{}'.format(dir[i]))
                for ingredient in recipe:
                    self.mats_req[ingredient] = recipe[ingredient] * multiplier
                    self.calc_mats_req(ingredient, multiplier)
    
    def calc_mats_missing(self):
        '''Calculates materials missing based on what's already in the inventory.'''
        inventory = File().json_to_dict('data/inventory.json')
        self.mats_missing = {}
        for ingredient in self.mats_req:
            if ingredient in inventory:
                qty_missing = self.mats_req[ingredient] - inventory[ingredient] 
                if qty_missing > 0:
                    self.mats_missing[ingredient] = qty_missing
            else:
                self.mats_missing[ingredient] = self.mats_req[ingredient]

    def retrieve_mats(self):
        '''Retrives list of materials required and missing; outputs it to their corresponding field.'''
        self.mats_req_textbox['state'] = NORMAL
        self.mats_missing_textbox['state'] = NORMAL

        self.mats_req = {}
        self.mats_req_textbox.delete('1.0', 'end')
        self.mats_missing_textbox.delete('1.0', 'end')

        self.calc_mats_req(self.selected_item.get(), self.multiplier.get())
        self.mats_req_textbox.insert('1.0', File().dict_to_text(self.mats_req))

        self.calc_mats_missing()
        self.mats_missing_textbox.insert('1.0', File().dict_to_text(self.mats_missing))

        self.mats_req_textbox['state'] = DISABLED
        self.mats_missing_textbox['state'] = DISABLED

    def start_job(self):
        item = self.job.get().lower()
        item_file = '{}.json'.format(item)
        dir = os.listdir('data/recipes')
        if item_file in dir: # checks if the item is a valid item
            self.calc_mats_req(item, self.quantity.get())
            # Gathers the name of the job and the materials it's using
            job_info = {
                'Name': item.title(),
                'Quantity': self.quantity.get(),
                'Materials Used': self.mats_req
            }

            self.add_job(job_info)

            self.job.set(value='')
            self.quantity.set(value=1)

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
        file = open('data/jobs/{}.json'.format(Crypto().generate_id()), 'w+')
        file.write(File().dict_to_json(info))
        file.close()
        self.load_jobs()
    
    def delete_job(self, file):
        os.remove('data/jobs/{}'.format(file))
        self.load_jobs()

class Job(ttk.Frame):
    def __init__(self, parent, file, order, delete_job, *args, **kwargs):
        '''A template frame for displaying information on a specific job'''
        super().__init__(parent, *args, **kwargs)

        job_file = File().json_to_dict('data/jobs/{}'.format(file))
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
        textbox.insert('1.0', File().dict_to_text(job_file['Materials Used']))
        textbox['state'] = DISABLED

        # * Button
        delete = ttk.Button(mainframe, text='Delete', command=lambda: delete_job(file))
        delete.grid(column=0, row=12, sticky=E)