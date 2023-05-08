import tkinter as tk

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

        return result
