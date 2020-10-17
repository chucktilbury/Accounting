from system.forms import Forms
from system.logger import *
from dialogs.edit_dialogs import *
from dialogs.select_dialog import *


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

        self.add_title('Browse Customers')

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
        self.add_indirect_label('country_ID', 1, 'Country', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Email:')
        self.add_dynamic_label('email_address', 1, bg='white', width=width2, anchor='w')
        self.add_label('Email Status:')
        self.add_indirect_label('email_status_ID', 1, 'EmailStatus', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Phone:')
        self.add_dynamic_label('phone_number', 1, bg='white', width=width2, anchor='w')
        self.add_label('Phone Status:')
        self.add_indirect_label('phone_status_ID', 1, 'PhoneStatus', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Web Site:')
        self.add_dynamic_label('web_site', 1, bg='white', width=width2, anchor='w')
        self.add_label('Class:')
        self.add_indirect_label('class_ID', 1, 'ContactClass', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Description:')
        self.add_dynamic_label('description', 3, bg='white', width=width1, anchor='w')

        self.add_label('Notes:')
        self.add_text('notes', 3, state='disabled', width=77, height=10)

        self.add_ctl_button('Prev')
        self.add_ctl_button('Next')
        self.add_btn_spacer()
        self.add_select_button(SelectDialog, owner=self.owner,
                                table=self.table, column='name')
        self.add_btn_spacer()
        self.add_ctl_button('Delete')
        self.add_custom_button('Edit', EditCustomerDialog, owner=self.owner,
                                table=self.table, row_index=self.row_index)
        self.add_custom_button('New', NewCustomerDialog, owner=self.owner,
                                table=self.table, row_index=self.row_index)


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

        self.add_title('Browse Vendors')

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
        self.add_indirect_label('country_ID', 1, 'Country', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Email:')
        self.add_dynamic_label('email_address', 1, bg='white', width=width2, anchor='w')
        self.add_label('Email Status:')
        self.add_indirect_label('email_status_ID', 1, 'EmailStatus', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Phone:')
        self.add_dynamic_label('phone_number', 1, bg='white', width=width2, anchor='w')
        self.add_label('Phone Status:')
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
        #self.add_ctl_button('Select', 'name')
        self.add_select_button(SelectDialog, owner=self.owner,
                                table=self.table, column='name')
        self.add_btn_spacer()
        self.add_ctl_button('Delete')
        self.add_custom_button('Edit', EditVendorDialog, owner=self.owner,
                                table=self.table, row_index=self.row_index)
        self.add_custom_button('New', NewVendorDialog, owner=self.owner,
                                table=self.table, row_index=self.row_index)

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
class SalesForm(Forms):

    def __init__(self, notebook):

        index = notebook.get_tab_index('Sales')
        super().__init__(notebook.frame_list[index]['frame'], 'SaleRecord')
        notebook.frame_list[index]['show_cb'] = self.load_form

        width2 = 25
        self.add_title('Browse Sales')

        self.add_label('Date:')
        self.add_dynamic_label('date', 1, bg='white', width=width2, anchor='w')
        self.add_spacer(2)

        self.add_label('Customer:')
        self.add_indirect_label('customer_ID', 1, 'Customer', 'name', bg='white', width=width2, anchor='w')

        self.add_label('Gross:')
        self.add_dynamic_label('gross', 1, bg='white', width=width2, anchor='w')

        self.add_label('Fees:')
        self.add_dynamic_label('fees', 1, bg='white', width=width2, anchor='w')

        self.add_label('Shipping:')
        self.add_dynamic_label('shipping', 1, bg='white', width=width2, anchor='w')

        self.add_label('Status:')
        self.add_indirect_label('status_ID', 1, 'SaleStatus', 'name', bg='white', width=width2, anchor='w')

        #self.add_products_widget()

        self.add_label('Committed:')
        self.add_checkbox('committed', state='disabled')

        self.add_label('Notes:')
        self.add_text('notes', 3, state='disabled', width=77, height=10)

        self.add_ctl_button('Prev')
        self.add_ctl_button('Next')
        self.add_btn_spacer()
        self.add_select_button(IndirectSelectDialog, owner=self.owner,
                                loc_tab=self.table, loc_col='customer_ID',
                                for_tab='Customer', for_col='name')
        self.add_btn_spacer()
        self.add_ctl_button('Delete')
        self.add_custom_button('Edit', EditSaleDialog, owner=self.owner,
                                table=self.table, row_index=self.row_index)
        self.add_custom_button('New', NewSaleDialog, owner=self.owner,
                                table=self.table, row_index=self.row_index)

@class_wrapper
class PurchaseForm(Forms):

    def __init__(self, notebook):

        index = notebook.get_tab_index('Purchases')
        super().__init__(notebook.frame_list[index]['frame'], 'PurchaseRecord')
        notebook.frame_list[index]['show_cb'] = self.load_form

        width2 = 28
        self.add_title('Browse Purchases')
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

        self.add_ctl_button('Prev')
        self.add_ctl_button('Next')
        self.add_btn_spacer()
        self.add_select_button(IndirectSelectDialog, owner=self.owner,
                                loc_tab=self.table, loc_col='vendor_ID',
                                for_tab='Vendor', for_col='name')
        self.add_btn_spacer()
        self.add_ctl_button('Delete')
        self.add_custom_button('Edit', EditPurchaseDialog, owner=self.owner,
                                table=self.table, row_index=self.row_index)
        self.add_custom_button('New', NewPurchaseDialog, owner=self.owner,
                                table=self.table, row_index=self.row_index)
