from system.forms import Forms
from system.logger import *
from dialogs.edit_dialogs import *


#
# TODO: A customer cannot be deleted if a committed sale exists. If a customer is
#       deleted, then all uncommitted sales are also deleted.
#
#       Show total committed and uncommitted sales for customer.
#
@class_wrapper
class CustomersForm(Forms):

    def __init__(self, notebook):
        self.logger.set_level(Logger.DEBUG)

        index = notebook.get_tab_index('Customers')
        self.logger.debug('tab index = %d'%(index))
        super().__init__(notebook.frame_list[index]['frame'], 'Customer')
        notebook.frame_list[index]['show_cb'] = self.load_form

        width1 = 70
        width2 = 28

        self.add_title('Customers Form')

        self.add_label('Date:')
        self.add_dynamic_label('date_created', 1, bg='white', width=width2, anchor='w')
        self.add_spacer(2)

        self.add_label('Name:')
        self.add_dynamic_label('name', 3, bg='white', width=width1, anchor='w')
        self.add_label('Address1:')
        self.add_dynamic_label('address1', 3, bg='white', width=width1, anchor='w')
        self.add_label('Address2:')
        self.add_dynamic_label('address2', 3, bg='white', width=width1, anchor='w')

        self.add_label('City:')
        self.add_dynamic_label('city', 1, bg='white', width=width2, anchor='w')
        self.add_label('State:')
        self.add_dynamic_label('state', 1, bg='white', width=width2, anchor='w')

        self.add_label('Zip Code:')
        self.add_dynamic_label('zip', 1, bg='white', width=width2, anchor='w')
        self.add_label('Country:')
        #self.add_combo('country_ID', 1, 'Country', 'name')
        self.add_indirect_label('country_ID', 1, 'Country', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Email:')
        self.add_dynamic_label('email_address', 1, bg='white', width=width2, anchor='w')
        self.add_label('Email Status:')
        #self.add_combo('email_status_ID', 1, 'EmailStatus', 'name')
        self.add_indirect_label('email_status_ID', 1, 'EmailStatus', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Phone:')
        self.add_dynamic_label('phone_number', 1, bg='white', width=width2, anchor='w')
        self.add_label('Phone Status:')
        #self.add_combo('phone_status_ID', 1, 'PhoneStatus', 'name')
        self.add_indirect_label('phone_status_ID', 1, 'PhoneStatus', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Web Site:')
        self.add_dynamic_label('web_site', 1, bg='white', width=width2, anchor='w')
        self.add_label('Class:')
        #self.add_combo('class_ID', 1, 'ContactClass', 'name')
        self.add_indirect_label('class_ID', 1, 'ContactClass', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Description:')
        self.add_dynamic_label('description', 3, bg='white', width=width1, anchor='w')

        self.add_label('Notes:')
        self.add_text('notes', 3, state='disabled', width=77, height=10)

        self.add_ctl_button('Prev')
        self.add_ctl_button('Next')
        self.add_btn_spacer()
        self.add_ctl_button('Select', 'name')
        self.add_btn_spacer()
        self.add_ctl_button('Delete')
        self.add_custom_button('Edit', EditCustomerDialog)
        self.add_custom_button('New', NewCustomerDialog)


#
# TODO: A vendor cannot be deleted if a committed purchase exists. If a vendor is
#       deleted, then all uncommitted purchases are also deleted.
#
#       Associate a vendor with an account. When a purchase is made, then that
#       account is debit when the purchase is committed.
#
#       Show total committed and uncommitted purchases for vendor
#
@class_wrapper
class VendorsForm(Forms):

    def __init__(self, notebook):
        self.logger.set_level(Logger.DEBUG)

        index = notebook.get_tab_index('Vendors')
        super().__init__(notebook.frame_list[index]['frame'], 'Vendor')
        notebook.frame_list[index]['show_cb'] = self.load_form

        width1 = 70
        width2 = 28

        self.add_title('Vendors Form')

        self.add_label('Date:')
        self.add_dynamic_label('date_created', 1, bg='white', width=width2, anchor='w')
        self.add_spacer(2)

        self.add_label('Name:')
        self.add_dynamic_label('name', 3, bg='white', width=width1, anchor='w')
        self.add_label('Contact Name:')
        self.add_dynamic_label('contact_name', 3, bg='white', width=width1, anchor='w')
        self.add_label('Address1:')
        self.add_dynamic_label('address1', 3, bg='white', width=width1, anchor='w')
        self.add_label('Address2:')
        self.add_dynamic_label('address2', 3, bg='white', width=width1, anchor='w')

        self.add_label('City:')
        self.add_dynamic_label('city', 1, bg='white', width=width2, anchor='w')
        self.add_label('State:')
        self.add_dynamic_label('state', 1, bg='white', width=width2, anchor='w')

        self.add_label('Zip Code:')
        self.add_dynamic_label('zip', 1, bg='white', width=width2, anchor='w')
        self.add_label('Country:')
        #self.add_combo('country_ID', 1, 'Country', 'name')
        self.add_indirect_label('country_ID', 1, 'Country', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Email:')
        self.add_dynamic_label('email_address', 1, bg='white', width=width2, anchor='w')
        self.add_label('Email Status:')
        #self.add_combo('email_status_ID', 1, 'EmailStatus', 'name')
        self.add_indirect_label('email_status_ID', 1, 'EmailStatus', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Phone:')
        self.add_dynamic_label('phone_number', 1, bg='white', width=width2, anchor='w')
        self.add_label('Phone Status:')
        #self.add_combo('phone_status_ID', 1, 'PhoneStatus', 'name')
        self.add_indirect_label('phone_status_ID', 1, 'PhoneStatus', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Web Site:')
        self.add_dynamic_label('web_site', 1, bg='white', width=width2, anchor='w')
        self.add_label('Type:')
        self.add_indirect_label('type_ID', 1, 'ContactClass', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Description:')
        self.add_dynamic_label('description', 3, bg='white', width=width1, anchor='w')

        self.add_label('Notes:')
        self.add_text('notes', 3, state='disabled', width=77, height=10)

        self.add_ctl_button('Prev')
        self.add_ctl_button('Next')
        self.add_btn_spacer()
        self.add_ctl_button('Select', 'name')
        self.add_btn_spacer()
        self.add_ctl_button('Delete')
        self.add_custom_button('Edit', EditVendorDialog)
        self.add_custom_button('New', NewVendorDialog)

#
# TODO: Modify these forms so that a new sale can be entered and committed sales
#       cannot be modified. (sales and products)
#
#       Need to select sales based on customer name and pull up all sales associated
#       a customer for selections.
#
#       Find a way to prevent duplicate sales from being imported.
#
#       Make product widget simpler. This form only displays the products. Products
#       for this sale are edited in a different dialog that is activated by a button.
#       If the sale is committed, then the button is disabled.
#
#       Sales and purchases need to show if they have been committed. When the commit
#       button is pressed, then the accounts are debited.
#
@class_wrapper
class sSalesForm(Forms):

    def __init__(self, notebook):
        super().__init__(notebook, notebook.get_tab_index('Sales'), 'SaleRecord')

        self.add_title('Sales Setup Form')
        self.add_indirect_label('Customer', 'customer_ID', 1, 'Customer', 'name')
        self.add_spacer(1)
        self.add_dynamic_label('Gross', 'gross', 1)
        self.add_spacer(1)
        self.add_dynamic_label('Fees', 'fees', 1)
        self.add_spacer(1)
        self.add_dynamic_label('Shipping', 'shipping', 1)
        self.add_spacer(1)
        self.add_combo('Status', 'status_ID', 1, 'SaleStatus', 'name')
        self.add_spacer(1)
        #self.add_products_widget()

        self.add_ctl_button('Prev')
        self.add_ctl_button('Next')
        self.add_btn_spacer()
        self.add_ctl_button('Save')
        self.add_ctl_button('Delete')
        #self.add_commit_btn()
        self.add_btn_spacer()
        self.add_edit_button('Edit Notes', 'notes', 'Notes')

@class_wrapper
class sPurchaseForm(Forms):

    def __init__(self, notebook):
        super().__init__(notebook, notebook.get_tab_index('Purchases'), 'PurchaseRecord')

        self.add_title('Purchase Setup Form')
        self.add_indirect_label('Vendor', 'vendor_ID', 1, 'Vendor', 'name')
        self.add_spacer(1)
        self.add_dynamic_label('Gross', 'gross', 1)
        self.add_spacer(1)
        self.add_dynamic_label('Tax', 'tax', 1)
        self.add_spacer(1)
        self.add_dynamic_label('Shipping', 'shipping', 1)
        self.add_spacer(1)
        self.add_combo('Purchase Type', 'type_ID', 1, 'PurchaseType', 'name')
        self.add_spacer(1)
        self.add_combo('Purchase Status', 'status_ID', 1, 'PurchaseStatus', 'name')
        self.add_spacer(1)

        self.add_ctl_button('Prev')
        self.add_ctl_button('Next')
        self.add_btn_spacer()
        self.add_ctl_button('Save')
        self.add_ctl_button('Delete')
        #self.add_commit_btn()
        self.add_btn_spacer()
        self.add_edit_button('Edit Notes', 'notes', 'Notes')
