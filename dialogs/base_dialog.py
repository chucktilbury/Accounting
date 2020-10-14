import tkinter as tk
from system.logger import *

@class_wrapper
class BaseFormDialog(tk.Toplevel):
    '''
    Display a text edit form and possibly save the results.
    '''

    def __init__(self, owner, form, table, row_index, column=None, thing=None):
        super().__init__(owner)
        self.transient(owner)

        if column is None:
            label = thing
        else:
            if thing is None:
                label = 'Edit Info'
            else:
                label = 'Edit ' + thing


        self.title(label)

        self.upper_frame = tk.Frame(self)
        self.upper_frame.grid(row=0, column=0)
        self.lower_frame = tk.LabelFrame(self)
        self.lower_frame.grid(row=1, column=0)

        if column is None:
            self.cf = form(self.upper_frame, row_index)
        else:
            self.cf = form(self.upper_frame, table, column, row_index, label)

        self.cf.grid()
        tk.Button(self.lower_frame, text='Dismiss', command=self._dismiss_btn).grid()
        #self.cf.load_form()
        self.wait_window(self)

    @func_wrapper
    def _dismiss_btn(self):
        self.cf.check_save()
        self.destroy()
