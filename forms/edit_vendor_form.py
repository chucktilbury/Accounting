from system.forms import Forms
from system.logger import *
#from dialogs.edit_dialogs import *
from dialogs.select_dialog import *

@class_wrapper
class _edit_vendor_form(Forms):

    def __init__(self, owner, row_index):
        self.logger.set_level(Logger.DEBUG)

        super().__init__(owner, 'Vendor')
        self.row_index = row_index

    def add_form(self):
        width1 = 70
        width2 = 28

        self.add_label('Date:')
        self.add_dynamic_label('date_created', 1, bg='white', width=width2, anchor='w')
        self.add_spacer(2)

        self.add_label('Name:')
        wid = self.add_entry('name', 3, str, width=width1)
        self.add_dupe_check(wid)

        self.add_label('Contact Name:')
        self.add_entry('contact_name', 3, str, width=width1)
        self.add_label('Address1:')
        self.add_entry('address1', 3, str, width=width1)
        self.add_label('Address2:')
        self.add_entry('address2', 3, str, width=width1)

        self.add_label('City:')
        self.add_entry('city', 1, str, width=width2)
        self.add_label('State:')
        self.add_entry('state', 1, str, width=width2)

        self.add_label('Zip Code:')
        self.add_entry('zip', 1, str, width=width2)
        self.add_label('Country:')
        self.add_combo('country_ID', 1, 'Country', 'name', width=width2)

        self.add_label('Email:')
        self.add_entry('email_address', 1, str, width=width2)
        self.add_label('Email Status:')
        self.add_combo('email_status_ID', 1, 'EmailStatus', 'name', width=width2)

        self.add_label('Phone:')
        self.add_entry('phone_number', 1, str, width=width2)
        self.add_label('Phone Status:')
        self.add_combo('phone_status_ID', 1, 'PhoneStatus', 'name', width=width2)

        self.add_label('Web Site:')
        self.add_entry('web_site', 1, str, width=width2)
        self.add_label('Vendor Type:')
        self.add_combo('type_ID', 1, 'VendorType', 'name', width=width2)

        self.add_label('Description:')
        self.add_entry('description', 3, str, width=width1)

        self.add_label('Notes:')
        self.add_text('notes', 3, width=77, height=10)

    def add_edit_buttons(self):
        self.add_ctl_button('Prev')
        self.add_ctl_button('Next')
        #self.add_ctl_button('Select', 'name')
        self.add_select_button(SelectDialog, owner=self.owner ,table=self.table, column='name')
        self.add_btn_spacer()
        self.add_ctl_button('Save')

    def add_new_buttons(self):
        self.add_ctl_button('Save', new_flag=True)

@class_wrapper
class EditVendorForm(_edit_vendor_form):
    '''
    '''
    def __init__(self, owner, row_index):
        self.logger.set_level(Logger.DEBUG)
        super().__init__(owner, row_index)

        self.add_title('Edit Vendor')
        self.add_form()
        self.add_edit_buttons()
        self.load_form()

@class_wrapper
class NewVendorForm(_edit_vendor_form):
    '''
    '''
    def __init__(self, owner, row_index):
        self.logger.set_level(Logger.DEBUG)
        super().__init__(owner, row_index)

        self.add_title('New Vendor')
        self.add_form()
        self.add_new_buttons()
        self.clear_form()
