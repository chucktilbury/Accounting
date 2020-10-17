from system.forms import Forms
from system.logger import *
from dialogs.select_dialog import *

@class_wrapper
class _edit_purch_form(Forms):

    def __init__(self, owner, row_index):
        self.logger.set_level(Logger.DEBUG)

        super().__init__(owner, 'PurchaseRecord')
        self.row_index = row_index

    def add_form(self):
        width2 = 28

        self.add_label('Date:')
        self.add_dynamic_label('date', 1, bg='white', width=width2, anchor='w')
        self.add_spacer(2)

        self.add_label('Vendor:')
        self.add_indirect_label('vendor_ID', 1, 'Vendor', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Gross:')
        self.add_dynamic_label('gross', 1, bg='white', width=width2, anchor='w')

        self.add_label('Tax:')
        self.add_dynamic_label('tax', 1, bg='white', width=width2, anchor='w')

        self.add_label('Shipping:')
        self.add_dynamic_label('shipping', 1, bg='white', width=width2, anchor='w')

        self.add_label('Type:')
        self.add_indirect_label('type_ID', 1, 'PurchaseType', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Status:')
        self.add_indirect_label('status_ID', 1, 'PurchaseStatus', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Committed:')
        self.add_checkbox('committed', state='disabled')
        self.add_spacer(2)

        self.add_label('Notes:')
        self.add_text('notes', 3, state='disabled', width=77, height=10)

    def add_edit_buttons(self):
        self.add_ctl_button('Prev')
        self.add_ctl_button('Next')
        self.add_select_button(IndirectSelectDialog, owner=self.owner,
                            loc_tab=self.table, loc_col='vendor_ID',
                            for_tab='Vendor', for_col='name')
        self.add_btn_spacer()
        self.add_ctl_button('Save')

    def add_new_buttons(self):
        self.add_ctl_button('Save', new_flag=True)

@class_wrapper
class NewPurchaseForm(_edit_purch_form):
    '''
    '''
    def __init__(self, owner, row_index):
        self.logger.set_level(Logger.DEBUG)
        super().__init__(owner, row_index)

        self.add_title('New Purchase')
        self.add_form()
        self.add_new_buttons()
        self.clear_form()


@class_wrapper
class EditPurchaseForm(_edit_purch_form):
    '''
    '''
    def __init__(self, owner, row_index):
        self.logger.set_level(Logger.DEBUG)
        super().__init__(owner, row_index)

        self.add_title('Edit Purchase')
        self.add_form()
        self.add_edit_buttons()
        self.load_form()
