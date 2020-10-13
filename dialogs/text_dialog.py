import tkinter as tk
from system.forms import Forms
from system.logger import *

@class_wrapper
class _text_form(Forms):

    def __init__(self, owner, table, column, row_index, label):
        super().__init__(owner, table, columns=1)

        self.row_index = row_index

        self.add_title('Edit %s'%(label))
        self.add_text(column, 1, width=70, height=20)
        self.add_ctl_button('Save')


@class_wrapper
class _text_dialog(tk.Toplevel):
    '''
    Display a text edit form and possibly save the results.
    '''

    def __init__(self, owner, table, column, row_index, thing=None):
        super().__init__(owner)
        self.transient(owner)

        if thing is None:
            label = 'Info'
        else:
            label = thing


        self.title('Edit %s'%(label))

        self.upper_frame = tk.Frame(self)
        self.upper_frame.grid(row=0, column=0)
        self.lower_frame = tk.LabelFrame(self)
        self.lower_frame.grid(row=1, column=0)

        self.cf = _text_form(self.upper_frame, table, column, row_index, label)
        self.cf.grid()
        tk.Button(self.lower_frame, text='Dismiss', command=self._dismiss_btn).grid()
        self.cf.load_form()
        self.wait_window(self)

    @func_wrapper
    def _dismiss_btn(self):
        self.cf.check_save()
        self.destroy()

@class_wrapper
class EditNotes(_text_dialog):

    def __init__(self, owner, table, column, row):
        super().__init__(owner, table, column, row, 'Notes')

@class_wrapper
class EditTerms(_text_dialog):

    def __init__(self, owner, table, column, row):
        super().__init__(owner, table, column, row, 'Terms')

@class_wrapper
class EditWarranty(_text_dialog):

    def __init__(self, owner, table, column, row):
        super().__init__(owner, table, column, row, 'Warranty')

@class_wrapper
class EditReturns(_text_dialog):

    def __init__(self, owner, table, column, row):
        super().__init__(owner, table, column, row, 'Returns')
