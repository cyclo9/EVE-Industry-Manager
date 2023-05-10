import tkinter as tk
from tkinter import *
from tkinter import ttk

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        """A text widget that reports on internal widget commands"""
        super().__init__(*args, **kwargs)

        # create a proxy for the underlying widget
        self._og = self._w + "_og"
        self.tk.call("rename", self._w, self._og)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        # avoid error when copying
        if command == 'get' and (args[0] == 'sel.first' and args[1] == 'sel.last') and not self.tag_ranges('sel'):
            return

        # avoid error when deleting
        if command == 'delete' and (args[0] == 'sel.first' and args[1] == 'sel.last') and not self.tag_ranges('sel'):
            return

        cmd = (self._og, command) + args
        result = self.tk.call(cmd)

        if command in ('insert', 'delete', 'replace'):
            self.event_generate('<<TextModified>>')

        if command in ('insert'):
            self.event_generate('<<TextInsert>>')

        return result
    
class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = Canvas(self, highlightthickness=0, *args, **kwargs)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel) # Bind mouse wheel event
        self.canvas.grid(row=0, column=0, sticky=NSEW)
        scrollbar.grid(row=0, column=1, sticky=NS)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _on_mousewheel(self, event):
        """Handle mouse wheel events."""
        # Scroll the canvas up or down depending on the direction of the wheel event
        if event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.delta < 0:
            self.canvas.yview_scroll(1, "units")