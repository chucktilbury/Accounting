from system.logger import *
from .base_dialog import BaseFormDialog
from forms.edit_customer_form import *
from forms.edit_vendor_form import *
from forms.edit_sale_form import *
from forms.edit_purchase_form import *

@class_wrapper
class EditCustomerDialog(BaseFormDialog):
    '''
    '''
    def __init__(self, owner, table, row_index):
        super().__init__(owner, EditCustomerForm, table, row_index, thing='Edit Customer')

@class_wrapper
class NewCustomerDialog(BaseFormDialog):
    '''
    '''
    def __init__(self, owner, table, row_index):
        super().__init__(owner, NewCustomerForm, table, row_index, thing='New Customer')

@class_wrapper
class EditVendorDialog(BaseFormDialog):
    '''
    '''
    def __init__(self, owner, table, row_index):
        super().__init__(owner, EditVendorForm, table, row_index, thing='Edit Vendor')

@class_wrapper
class NewVendorDialog(BaseFormDialog):
    '''
    '''
    def __init__(self, owner, table, row_index):
        super().__init__(owner, NewVendorForm, table, row_index, thing='New Vendor')

@class_wrapper
class EditPurchaseDialog(BaseFormDialog):
    '''
    '''
    def __init__(self, owner, table, row_index):
        super().__init__(owner, EditPurchaseForm, table, row_index, thing='Edit Purchase')

@class_wrapper
class NewPurchaseDialog(BaseFormDialog):
    '''
    '''
    def __init__(self, owner, table, row_index):
        super().__init__(owner, NewPurchaseForm, table, row_index, thing='New Purchase')

@class_wrapper
class EditSaleDialog(BaseFormDialog):
    '''
    '''
    def __init__(self, owner, table, row_index):
        super().__init__(owner, EditSaleForm, table, row_index, thing='Edit Sale')

@class_wrapper
class NewSaleDialog(BaseFormDialog):
    '''
    '''
    def __init__(self, owner, table, row_index):
        super().__init__(owner, NewSaleForm, table, row_index, thing='New Sale')
