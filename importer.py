
from tkinter.messagebox import showwarning, showerror, showinfo
import sys, os, csv
from database import Database
from logger import *


@class_wrapper
class ImportPayPal(object):
    '''
    This class imports a PayPal CSV file into the database.
    '''

    def __init__(self, fname):

        self.fname = fname
        self.data = Database.get_instance()
        self.accepted = 0
        self.rejected = 0
        self.logger.set_level(Logger.DEBUG)

        self.legend = [
            'Date',
            'Time',
            'TimeZone',
            'Name',
            'Type',
            'Status',
            'Currency',
            'Gross',
            'Fee',
            'Net',
            'FromEmail',
            'ToEmail',
            'TransactionID',
            'ShippingAddress',
            'AddressStatus',
            'ItemTitle',
            'ItemID',
            'Shipping',
            'InsuranceAmount',
            'SalesTax',
            'Option1Name',
            'Option1Value',
            'Option2Name',
            'Option2Value',
            'ReferenceTxnID',
            'InvoiceNumber',
            'CustomNumber',
            'Quantity',
            'ReceiptID',
            'Balance',
            'AddressLine1',
            'AddressLine2',
            'City',
            'State',
            'PostalCode',
            'Country',
            'Phone',
            'Subject',
            'Note',
            'CountryCode',
            'BalanceImpact']

    @func_wrapper
    def import_all(self):
        '''
        This is the top level interface for the importer. All of the other methods
        are private.
        '''
        # import the CSV file into the database.
        try:
            self._read_file()
            # get the various tables set up
            codes = self._countries()
            cust = self._customers()
            vend = self._vendors()
            sales = self._sales()
            purch = self._purchases()

            text = 'Imported records:\n'
            text += '   %d country codes\n'%(codes)
            text += '   %d unique customer entries\n'%(cust)
            text += '   %d unique vendor entries\n'%(vend)
            text += '   %d sale entries\n'%(sales)
            text += '   %d purchase entries\n'%(purch)
            text += '   %d CSV lines accepted\n'%(self.accepted)
            text += '   %d CSV lines rejected\n'%(self.rejected)

            showinfo('Import', text)

        except Exception:
            showerror("ERROR", 'Could not import file: "%s"'%(self.fname))

    @func_wrapper
    def _read_file(self):
        '''
        Read the CSV file into an array of lines where each one is a dictionary with the
        column names as keys.
        '''
        with open(self.fname, "r") as fh:
            reader = csv.reader(fh)

            line = []
            for line in reader:
                break

            if not line[1] == 'Time':
                raise('File selected is not a PayPal CSV import file.')


            for line in reader:
                rec = {}
                for idx, item in enumerate(line):
                    #if item == '':
                    #    rec[self.legend[idx]] = None
                    #else:
                    rec[self.legend[idx]] = item
                    rec['imported_country'] = False
                    rec['imported_customer'] = False
                    rec['imported_vendor'] = False
                    rec['imported_sale'] = False
                    rec['imported_purchase'] = False

                if not self.data.if_rec_exists('RawImport', 'TransactionID', rec['TransactionID']):
                    self.data.insert_row('RawImport', rec)
                    self.accepted += 1
                else:
                    self.rejected += 1

            self.data.commit()

    @func_wrapper
    def _countries(self):
        '''
        Read the new import and copy new country codes into the country codes table.
        '''
        data = self.data.get_row_list('RawImport', 'imported_country = false')
        if data is None:
            return 0

        count = 0
        for item in data:
            if item['CountryCode'] != '' and not self.data.if_rec_exists('Country', 'abbreviation', item['CountryCode']):
                rec = {'name': item['Country'],
                        'abbreviation': item['CountryCode']}
                self.data.insert_row('Country', rec)
                count += 1
            self.data.update_row_by_id('RawImport', {'imported_country':True}, item['ID'])

        self.data.commit()
        return count

    @func_wrapper
    def _customers(self):
        '''
        Find all of the new customer records and copy the data into the customers table.
        '''
        data = self.data.get_row_list('RawImport', 'imported_customer = false and BalanceImpact = \'Credit\'')
        if data is None:
            showinfo('INFO', 'There are no customer contacts to import.')
            return 0

        count = 0
        for item in data:
            if item['Type'] == 'Website Payment' or item['Type'] == 'General Payment':
                # Yes it's a customer
                if not self.data.if_rec_exists('Customer', 'name', item['Name']):
                    rec = { 'date_created': item['Date'],
                            'name': item['Name'],
                            'address1': item['AddressLine1'],
                            'address2': item['AddressLine2'],
                            'state': item['State'],
                            'city': item['City'],
                            'zip': item['PostalCode'],
                            'email_address': item['FromEmail'],
                            'email_status_ID': self.data.get_id_by_row('EmailStatus', 'name', 'primary'),
                            'phone_number': item['Phone'],
                            'phone_status_ID': self.data.get_id_by_row('PhoneStatus', 'name', 'primary'),
                            'description': 'Imported from PayPal',
                            'notes': item['Subject'],
                            'country_ID': self.data.get_id_by_row('Country', 'abbreviation', item['CountryCode']),
                            'class_ID': self.data.get_id_by_row('ContactClass', 'name', 'retail')}

                    self.data.insert_row('Customer', rec)
                    count+=1
                # BUG: (fixed) When there are multiple instances of a name, the sale or purch record does not get imported
                # because the imported_customer field does not get updated due to the duplicate name interlock.
                self.data.update_row_by_id('RawImport', {'imported_customer':True}, item['ID'])
        self.data.commit()
        return count

    @func_wrapper
    def _vendors(self):
        '''
        Find all of the new vendor records and copy the data into the vendor table.
        '''
        data = self.data.get_row_list('RawImport', 'imported_vendor = false and BalanceImpact = \'Debit\'')
        if data is None:
            showinfo('INFO', 'There are no customer contacts to import.')
            return 0

        count = 0
        for item in data:
            if item['Name'] != '' and item['Name'] != 'PayPal':
                if not self.data.if_rec_exists('Vendor', 'name', item['Name']):
                    rec = { 'date_created': item['Date'],
                            'name': item['Name'],
                            'contact_name':'',
                            'email_address': item['ToEmail'],
                            'email_status_ID': self.data.get_id_by_row('EmailStatus', 'name', 'primary'),
                            'phone_number': '',
                            'phone_status_ID': self.data.get_id_by_row('PhoneStatus', 'name', 'primary'),
                            'description': item['ItemTitle'],
                            'notes': item['Subject'],
                            'type_ID': self.data.get_id_by_row('VendorType', 'name', 'unknown'),}

                    self.data.insert_row('Vendor', rec)
                    self.data.update_row_by_id('RawImport', {'imported_vendor':True}, item['ID'])
                    count+=1

        self.data.commit()
        return count

    @func_wrapper
    def _sales(self):
        '''
        Find the sales records and copy the data into the sales database table.
        '''
        data = self.data.get_row_list('RawImport', 'imported_sale = false and imported_customer = true and BalanceImpact = \'Credit\'')
        if data is None:
            showinfo('INFO', 'There are no sales transcations to import.')
            return 0

        count = 0
        for item in data:
            if item['Name'] != '' and item['Name'] != 'PayPal':
                rec = { 'date': item['Date'],
                        'customer_ID': self.data.get_id_by_row('Customer', 'name', item['Name']),
                        'raw_import_ID': int(item['ID']),
                        'status_ID': self.data.get_id_by_row('SaleStatus', 'name', 'complete'),
                        'transaction_uuid': item['TransactionID'],
                        'gross': self.data.convert_value(item['Gross'], float),
                        'fees': self.data.convert_value(item['Fee'], float),
                        'shipping': self.data.convert_value(item['Shipping'], float),
                        'notes': item['Subject'] + '\n' +item['ItemTitle'],
                        'committed': False}

                self.data.insert_row('SaleRecord', rec)
                count+=1
                self.data.update_row_by_id('RawImport', {'imported_sale':True}, item['ID'])

        self.data.commit()
        return count

    @func_wrapper
    def _purchases(self):
        '''
        Find all of the purchase records and copy the data into the purchase database table.
        '''
        data = self.data.get_row_list('RawImport', 'imported_purchase = false and imported_vendor = true and BalanceImpact = \'Debit\'')
        if data is None:
            showinfo('INFO', 'There are no purchase transcations to import.')
            return 0

        count = 0
        for item in data:
            if item['Name'] != '' and item['Name'] != 'PayPal':
                gross = item['Gross']
                tax = item['SalesTax']
                shipping = item['Shipping']
                rec = { 'date': item['Date'],
                        'raw_import_ID': int(item['ID']),
                        'vendor_ID': self.data.get_id_by_row('Vendor', 'name', item['Name']),
                        'status_ID': self.data.get_id_by_row('PurchaseStatus', 'name', 'complete'),
                        'type_ID': self.data.get_id_by_row('PurchaseType', 'name', 'unknown'),
                        'transaction_uuid': item['TransactionID'],
                        'gross': self.data.convert_value(item['Gross'], float),
                        'tax': self.data.convert_value(item['SalesTax'], float),
                        'shipping': self.data.convert_value(item['Shipping'], float),
                        'notes': item['Subject'] + '\n' +item['ItemTitle'],
                        'committed': False}

                self.data.insert_row('PurchaseRecord', rec)
                self.data.update_row_by_id('RawImport', {'imported_purchase':True}, item['ID'])
                count+=1

        self.data.commit()
        return count
