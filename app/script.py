from tkinter import *
from tkinter import ttk
import os

from modules import File, Crypto
from widgets import H_ScrollableFrame
from tabs import Manager, Jobs

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
        jobs_tab = Jobs(self.n)
        self.n.add(Manager(self.n, jobs_tab.add_job), text='Manager')

        # * Jobs Page
        self.n.add(jobs_tab, text='Jobs')

        # for job_file in os.listdir('data/jobs'):
        #     name = job_file.split('.json')[0]
        #     job_info = File().json_to_dict('data/jobs/{}'.format(job_file))
        #     new_job = Job(self.n, self.delete_job, name, job_info)
        #     self.n.add(new_job, text=name)

    # def add_job(self, quantity, item, job_info):
    #     '''Creates a new Job tab.'''
    #     job_id = Crypto().generate_id()
    #     name = '{} (x{}) {}'.format(item.title(), quantity, job_id)

    #     # Saves the job_info into a file
    #     file = open('data/jobs/{}.json'.format(name), 'w+')
    #     file.write(File().dict_to_json(job_info))
    #     file.close()

    #     # Adds a new Job tab
    #     new_job = Job(self.n, self.delete_job, name, job_info)
    #     self.n.add(new_job, text=name)

    # def delete_job(self, tab_name):
    #     '''Deletes the current Job tab'''
    #     for tab in self.n.tabs():
    #         if self.n.tab(tab, "text") == tab_name:
    #             self.n.forget(tab)
    #             os.remove('data/jobs/{}.json'.format(tab_name))
    #             break

if __name__ == '__main__':
    App(root)
    root.mainloop()