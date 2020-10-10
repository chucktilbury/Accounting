import tkinter as tk
from forms import Forms

class _text_form(Forms):

    def __init__(self, owner, table, column, row_index):
        super().__init__(owner, table, columns=1)

        self.row_index = row_index

        self.add_title('Edit Notes')
        self.add_text('description', 1, width=70, height=20)
        self.add_ctl_button('Save')


class TextDialog(tk.Toplevel):
    '''
    Display a text edit form and possibly save the results.
    '''

    def __init__(self, owner, table, column, row_index):
        super().__init__(owner)
        self.transient(owner)
        self.title('Notes')

        self.upper_frame = tk.Frame(self)
        self.upper_frame.grid(row=0, column=0)
        self.lower_frame = tk.LabelFrame(self)
        self.lower_frame.grid(row=1, column=0)

        self.cf = _text_form(self.upper_frame, table, column, row_index)
        self.cf.grid()
        tk.Button(self.lower_frame, text='Dismiss', command=self._dismiss_btn).grid()
        self.cf.load_form()
        self.wait_window(self)

    def _dismiss_btn(self):
        self.cf.check_save()
        self.destroy()
