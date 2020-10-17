from system.forms import Forms
from system.logger import *
from dialogs.text_dialog import *
from dialogs.select_dialog import *

@class_wrapper
class BusinessForm(Forms):
    '''
    Create the form for the Business tab under Setup.
    '''

    def __init__(self, notebook):
        self.logger.set_level(Logger.DEBUG)

        index = notebook.get_tab_index('Business')
        super().__init__(notebook.frame_list[index]['frame'], 'Business', columns=4)
        notebook.frame_list[index]['show_cb'] = self.load_form

        wid = 50

        self.add_title('Business Setup Form')
        self.add_label('Name:')
        self.add_entry('name', 3, str, width=wid)
        self.add_label('Address1:')
        self.add_entry('address1', 3, str, width=wid)
        self.add_label('Address2:')
        self.add_entry('address2', 3, str, width=wid)

        self.add_label('City:')
        self.add_entry('city', 1, str)
        self.add_label('State:')
        self.add_entry('state', 1, str)

        self.add_label('Post Code:')
        self.add_entry('zip', 1, str)
        self.add_label('Country:')
        self.add_entry('country', 1, str)

        self.add_label('Email:')
        self.add_entry('email_address', 1, str)
        self.add_label('Phone:')
        self.add_entry('phone_number', 1, str)

        self.add_label('Web Site:')
        self.add_entry('web_site', 3, str, width=wid)
        self.add_label('Description:')
        self.add_entry('description', 3, str, width=wid)

        self.add_ctl_button('Save')
        self.add_btn_spacer()
        self.add_edit_button('Edit Terms', 'terms', EditTerms)
        self.add_edit_button('Edit Returns', 'returns', EditReturns)
        self.add_edit_button('Edit Warranty', 'warranty', EditWarranty)

@class_wrapper
class AccountsForm(Forms):

    def __init__(self, notebook):
        self.logger.set_level(Logger.DEBUG)

        index = notebook.get_tab_index('Accounts')
        super().__init__(notebook.frame_list[index]['frame'], 'Account')
        notebook.frame_list[index]['show_cb'] = self.load_form

        wid = 52
        self.add_title('Accounts Setup Form')

        self.add_label('Name:')
        self.add_entry('name', 1, str)
        self.add_label('Number:')
        self.add_entry('number', 1, str)

        self.add_label('Account Type:')
        self.add_combo('type_ID', 1, 'AccountTypes', 'name')
        self.add_label('Balance:')
        self.add_entry('total', 1, float)
        self.add_label('Description:')

        self.add_entry('description', 3, str, width=wid)

        self.add_ctl_button('Prev')
        self.add_ctl_button('Next')
        self.add_btn_spacer()
        #self.add_ctl_button('Select', 'name')
        self.add_select_button(SelectDialog, owner=self.owner ,table=self.table, column='name')
        self.add_ctl_button('Clear')
        self.add_ctl_button('Save')
        self.add_ctl_button('Delete')
        self.add_btn_spacer()
        self.add_edit_button('Edit Notes', 'notes', EditNotes)

@class_wrapper
class InventoryForm(Forms):

    def __init__(self, notebook):
        self.logger.set_level(Logger.DEBUG)

        index = notebook.get_tab_index('Inventory')
        super().__init__(notebook.frame_list[index]['frame'], 'InventoryItem')
        notebook.frame_list[index]['show_cb'] = self.load_form

        wid = 52
        self.add_title('Inventory Setup Form')

        self.add_label('Name:')
        self.add_entry('name', 3, str, width=wid)

        self.add_label('Stock Num:')
        self.add_entry('stock_num', 1, int)
        self.add_label('Quantity:')
        self.add_entry('num_stock', 1, int)

        self.add_label('Retail Price:')
        self.add_entry('retail', 1, float)
        self.add_label('Wholesale:')
        self.add_entry('wholesale', 1, float)

        self.add_label('Description:')
        self.add_entry('description', 3, str, width=wid)

        self.add_ctl_button('Prev')
        self.add_ctl_button('Next')
        self.add_btn_spacer()
        #self.add_ctl_button('Select', 'name')
        self.add_select_button(SelectDialog, owner=self.owner ,table=self.table, column='name')
        self.add_ctl_button('Clear')
        self.add_ctl_button('Save')
        self.add_ctl_button('Delete')
        self.add_btn_spacer()
        self.add_edit_button('Edit Notes', 'notes', EditNotes)

