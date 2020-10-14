import tkinter as tk
from system.forms import Forms
from system.logger import *
from .base_dialog import BaseFormDialog

@class_wrapper
class _text_form(Forms):

    def __init__(self, owner, table, column, row_index, label):
        super().__init__(owner, table, columns=1)

        self.row_index = row_index

        self.add_title('Edit %s'%(label))
        self.add_text(column, 1, width=70, height=20)
        self.add_ctl_button('Save')

@class_wrapper
class EditNotes(BaseFormDialog):

    def __init__(self, owner, table, column, row):
        super().__init__(owner, _text_form, table, row, column, 'Notes')
        self.load_form()

@class_wrapper
class EditTerms(BaseFormDialog):

    def __init__(self, owner, table, column, row):
        super().__init__(owner, _text_form, table, row, column, 'Terms')
        self.load_form()

@class_wrapper
class EditWarranty(BaseFormDialog):

    def __init__(self, owner, table, column, row):
        super().__init__(owner, _text_form, table, row, column, 'Warranty')
        self.load_form()

@class_wrapper
class EditReturns(BaseFormDialog):

    def __init__(self, owner, table, column, row):
        super().__init__(owner, _text_form, table, row, column, 'Returns')
        self.load_form()
