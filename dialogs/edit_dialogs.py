from system.logger import *
from .base_dialog import BaseFormDialog
from forms.edit_customer_form import *
from forms.edit_vendor_form import *

@class_wrapper
class EditCustomerDialog(BaseFormDialog):
    '''
    '''
    def __init__(self, owner, table, row):
        super().__init__(owner, EditCustomerForm, table, row, thing='Edit Customer')

@class_wrapper
class NewCustomerDialog(BaseFormDialog):
    '''
    '''
    def __init__(self, owner, table, row):
        super().__init__(owner, NewCustomerForm, table, row, thing='New Customer')

@class_wrapper
class EditVendorDialog(BaseFormDialog):
    '''
    '''
    def __init__(self, owner, table, row):
        super().__init__(owner, EditVendorForm, table, row, thing='Edit Vendor')

@class_wrapper
class NewVendorDialog(BaseFormDialog):
    '''
    '''
    def __init__(self, owner, table, row):
        super().__init__(owner, NewVendorForm, table, row, thing='Edit Vendor')
