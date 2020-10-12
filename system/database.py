'''
This is a stub for the database. It exists to allow the formWidgets to be tested. There is no actual
database functionality in this file, but it does provide a template for implementing a real database
that interfaces to the form widgets.
'''
import sqlite3 as sql
import os, time, locale
from tkinter.messagebox import showerror
from system.logger import *

@class_wrapper
class Database(object):

    __instance = None

    @staticmethod
    def get_instance():
        if Database.__instance == None:
            Database()
        return Database.__instance

    def __init__(self):

        self.logger.set_level(Logger.DEBUG)
        if Database.__instance is None:
            Database.__instance = self
        else:
            raise Exception('The Database class is a singleton. Use get_instance() instead.')

        # put the stuff here to open the database file and all.
        self.data_version = '1.0'
        self.database_name = 'accounting.db'
        # self.database_name = 'sql/testing.db'
        # self.db_create_file = 'sql/database.sql'
        # self.db_pop_file = 'sql/populate.sql'
        self.open()

    @func_wrapper
    def open(self):
        '''
        High level database open routine. Handles creating the database if it's not found.
        '''
        # if not os.path.isfile(self.database_name):
        #     self.create_database()

        self.db = sql.connect(self.database_name)
        self.db.row_factory = sql.Row
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        self.db.execute('PRAGMA case_sensitive_like = false;')

    @func_wrapper
    def close(self):
        '''
        Close the database after committing all of the changes.
        '''
        self.db.commit()
        self.db.close()

    # @func_wrapper
    # def read_statement(self, fh):
    #     '''
    #     Read a statement from the *.sql file and return it. This skips comments and concatinates lines
    #     until a ';' is read.

    #     A comment is text that starts with a '#' and continues to the end of the line.
    #     '''
    #     retv = ''
    #     for line in fh:
    #         # strip comments from the line
    #         idx = line.find('#')
    #         line = line[0:idx].strip()
    #         # If there is anything left, append it to the return value.
    #         if len(line) > 0:
    #             retv += " %s"%(line)
    #             if line[-1] == ';':
    #                 break

    #     return retv

    # @func_wrapper
    # def run_file(self, db, name):
    #     '''
    #     Execute all of the statements in a *.sql file.
    #     '''
    #     with open(name) as fh:
    #         while True:
    #             line = self.read_statement(fh)
    #             if len(line) > 0:
    #                 #print(line)
    #                 db.execute(line)
    #             else:
    #                 break

    # @func_wrapper
    # def create_database(self):
    #     '''
    #     Create the database if it does not exist already.
    #     '''
    #     # Load the DB creation file and create the database from that.

    #     c = sql.connect(self.database_name)
    #     db = c.cursor()
    #     self.run_file(db, self.db_create_file)
    #     self.run_file(db, self.db_pop_file)
    #     c.commit()
    #     c.close()

    @func_wrapper
    def commit(self):
        '''
        Commit all changes to the database.
        '''
        self.db.commit()

    @func_wrapper
    def execute(self, _sql, data = None):
        '''
        Execute a single SQL statement.
        '''
        #print('execute: sql = %s, data = %s'%(sql, str(data)))
        try:
            if data is None:
                return self.db.execute(_sql)
            else:
                return self.db.execute(_sql, data)
        except sql.IntegrityError as e:
            showerror('ERROR', str(e))

    @func_wrapper
    def read_single_value(self, table, column, row_id):
        '''
        Read a single value from the database.
        '''
        if row_id is None:
            raise Exception('Cannot get item from database: No row ID is set')

        sql = 'SELECT %s FROM %s WHERE ID=%d;'%(column, table, row_id)
        curs = self.execute(sql)
        recs = curs.fetchall()

        retv = None
        for row in recs:
            retv =  row[0]
            break

        return retv

    @func_wrapper
    def write_single_value(self, table, column, row_id, value):
        '''
        Write a single value to the database.
        '''
        vals = tuple([value])
        sql = 'UPDATE %s SET %s=? WHERE ID=%d;'%(table, column, row_id)

        return self.execute(sql, vals)

    @func_wrapper
    def get_column_list(self, table, column):
        '''
        Returns a list of column values in all lines of the table.
        '''
        curs = self.execute('SELECT %s FROM %s;'%(column, table))
        retv = []
        for item in curs:
            retv.append(' '.join(item))
        return retv

    @func_wrapper
    def get_row_id(self, table, column, value):
        '''
        Find the ID of the row that has this column value. If there are
        more than one row that has this value, then the a dictionary of
        the rows is returned. If there are no matches then return None.
        '''
        if type(value) is str:
            sql = 'SELECT ID FROM %s WHERE %s = \"%s\";'%(table, column, value)
        else:
            sql = 'SELECT ID FROM %s WHERE %s = %s;'%(table, column, value)
        row = self.execute(sql).fetchall()

        if len(row) == 0:
            return None
        else:
            return dict(row[0])['ID']

    @func_wrapper
    def get_id_list(self, table, where=None):
        '''
        Get a list of all IDs in a table. This is used (generally) to implement
        next and previous buttons in a form.
        '''
        retv = []
        if where is None:
            sql = 'SELECT ID FROM %s;'%(table)
        else:
            sql = 'SELECT ID FROM %s WHERE %s;'%(table, where)
        cur = self.execute(sql)
        for item in cur:
            retv.append(item[0])

        return retv

    @func_wrapper
    def get_id_by_column(self, table, column, val):
        '''
        Return a dictionary of the columns in the row where a data element matches the
        value given.
        '''
        if type(val) is str:
            sql = 'SELECT ID FROM %s WHERE %s = \"%s\";'%(table, column, val)
        else:
            sql = 'SELECT ID FROM %s WHERE %s = %s;'%(table, column, val)
        row = self.execute(sql).fetchall()

        if len(row) == 0:
            return None
        else:
            return dict(row[0])['ID']

    @func_wrapper
    def insert_row(self, table, data):
        '''
        Insert a row into the database. The data parameter is a dictionary where the
        keys are the names of the columns and the value is the value to place in the
        column.
        '''
        keys = ','.join(data.keys())
        qmks = ','.join(list('?'*len(data)))
        vals = tuple(data.values())

        try:
            line = 'INSERT INTO %s (%s) VALUES (%s);'%(table, keys, qmks)
            cur = self.db.execute(line, vals).lastrowid
            #print(str(cur))
            return cur
        except sql.IntegrityError as e:
            showerror('ERROR', str(e))
            return None

    @func_wrapper
    def delete_row(self, table, row_id):
        '''
        Delete the row with the given ID.
        '''
        sql = 'DELETE FROM %s WHERE ID = %d;' % (table, row_id)
        return self.db.execute(sql)

    @func_wrapper
    def check_dups(self, table, column, value):
        '''
        Return a list of rows that look similar to the value for that column.
        The '%' wildcard is added to both ends of the value and all spaces in
        value are replaced with the '%'. This is a very general search.
        '''
        if type(value) is str:
            val = ' '.join(value.split())   # get rid of duplicate spaces
            val = val.replace(' ', '%')     # replace the spaces with '%'
            where = '%'+str(value)+'%'
            line = 'SELECT * FROM %s WHERE %s LIKE \'%s\''%(table, column, where)
        else:
            where = '%'+str(value)+'%' #'%s%s%s'%('%', str(value), '%') # enclose the result in '%'s
            line = 'SELECT * FROM %s WHERE %s LIKE %s'%(table, column, where)

        print(line)
        cur = self.db.execute(line)
        retv = []
        for item in cur:
            retv.append(dict(item))

        return retv