'''
This is the main implementation file for the form widgets. These widgest are designed
to give clean and automated access to a database. The Database class is assumed to
already have the database open and ready to use.

These widgets are intended to be used with the forms module that is included in this
source code.
'''
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from tkinter.messagebox import *
from system.database import Database
from system.logger import *

class toolTip:
    '''
    This class binds a tool tip to a widget.
    '''

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)

    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background='yellow', relief='solid', borderwidth=1,
                       font=("times", "10", "normal"))
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()

@class_wrapper
class _form_widget_base(tk.Frame):
    '''
    This class implements the basic functions for all of the form widgets and
    invokes the database.
    '''

    def __init__(self, owner, table, column):
        super().__init__(owner)
        self.logger.set_level(Logger.DEBUG)
        self.data = Database.get_instance()
        self.owner = owner
        self.table = table
        self.column = column
        self.row_id = None
        self.changed = False

    @func_wrapper
    def getter(self):
        '''
        Stub function. The getter reads the widget and saves the data into the database as
        a single row/column entry.
        '''

    @func_wrapper
    def setter(self):
        '''
        Stub function. The setter reads the database as a single row/column entry and saves
        it into the widget.
        '''

    @func_wrapper
    def clear(self):
        '''
        Clears the widget.
        '''

    @func_wrapper
    def populate(self):
        '''
        For compound widgets, this can grab a list from the database and place it into the
        widget. For other widgets, it simply does the same as a setter().
        '''
        self.setter()

    @func_wrapper
    def get_insert_value(self):
        '''
        This is used when inserting a new row into the database.
        '''
        return self.column, self._read_value()

    @func_wrapper
    def _read_value(self):
        '''
        This is a "regular" way to obtain the value of a widget. This method must have an
        override. It's not supported for fields that have no getter().
        '''
        raise Exception('The _read_value method not supported for this widget.')

    @func_wrapper
    def set_row_id(self, row_id):
        '''
        This must be called before the value of the widget can be read or written.
        '''
        self.row_id = row_id

    @func_wrapper
    def is_changed(self, clear_flag=False):
        '''
        Return whether the control has changed or not.
        '''
        val = self.changed
        if clear_flag:
            self.changed = False
        return val

    @func_wrapper
    def get_column(self):
        '''
        Return the column.
        '''
        return self.column

    @func_wrapper
    def get_table(self):
        '''
        Return the table.
        '''
        return self.table

    @func_wrapper
    def check_dupes(self):
        '''
        Check for duplicate entries using the table and column along with the value
        held by the widget. Returns a list of dicts containg the entire rows where
        the data in the coumn might match. If there are no matches, then returns
        an empty list
        '''
        return self.data.check_dups(self.table, self.column, self._read_value())

    @func_wrapper
    def _bind_key(self, event=None):
        '''
        Callback for key binding to detect if widget has changed.
        '''
        self.changed = True

@class_wrapper
class formEntry(_form_widget_base):
    '''
    Wrapper for the tkinter Entry widget.
    '''

    def __init__(self, owner, table, column, _type, tool_tip=None, **kw):
        super().__init__(owner, table, column)
        self.logger.set_level(Logger.DEBUG)
        self._type = _type

        self.value = tk.StringVar(self)
        self.widget = tk.Entry(self, textvariable=self.value, **kw)
        self.widget.grid()
        self.widget.bind('<Key>', self._bind_key)
        if not tool_tip is None:
            self.tool_tip = toolTip(self, tool_tip)

    @func_wrapper
    def getter(self):
        val = self._read_value()
        self.data.write_single_value(self.table, self.column, self.row_id, val)

    @func_wrapper
    def setter(self):
        state = self.widget.configure()['state']
        if state == 'readonly':
            self.widget.configure(state='normal')

        val = self.data.read_single_value(self.table, self.column, self.row_id)
        if val is None:
            self.value.set('')
        else:
            self.value.set(str(val))

        if state == 'readonly':
            self.widget.configure(state='readonly')

    @func_wrapper
    def clear(self):
        state = self.widget.configure()['state']
        if state == 'readonly':
            self.widget.configure(state='normal')

        self.value.set('')

        if state == 'readonly':
            self.widget.configure(state='readonly')

    @func_wrapper
    def _read_value(self):
        val = self._type(self.value.get())
        # This enforces the NOT NULL clause in the database structure
        if val == '':
            return None
        else:
            return val

@class_wrapper
class formText(_form_widget_base):

    def __init__(self, owner, table, column, tool_tip=None, **kw):
        super().__init__(owner, table, column)
        self.logger.set_level(Logger.DEBUG)

        self.local_frame = tk.Frame(self, bd=1, relief=tk.RIDGE)
        self.widget = tk.Text(self.local_frame, wrap=tk.NONE, **kw)
        self.widget.insert(tk.END, '')
        self.widget.grid(row=0, column=0, sticky='nw')

        self.vsb = tk.Scrollbar(self.local_frame, orient=tk.VERTICAL)
        self.vsb.config(command=self.widget.yview)
        self.widget.config(yscrollcommand=self.vsb.set)
        self.vsb.grid(row=0, column=1, sticky='nse')

        self.hsb = tk.Scrollbar(self.local_frame, orient=tk.HORIZONTAL)
        self.hsb.config(command=self.widget.xview)
        self.widget.config(xscrollcommand=self.hsb.set)
        self.hsb.grid(row=1, column=0, sticky='wes')

        self.local_frame.grid(row=0, column=1, sticky='w')
        self.widget.bind('<Key>', self._bind_key)
        if not tool_tip is None:
            self.tool_tip = toolTip(self, tool_tip)

    @func_wrapper
    def getter(self):
        value = self._read_value()
        self.data.write_single_value(self.table, self.column, self.row_id, value)

    @func_wrapper
    def setter(self):
        value = self.data.read_single_value(self.table, self.column, self.row_id)
        self.widget.delete('1.0', tk.END)
        if not value is None:
            self.widget.insert(tk.END, str(value))

    @func_wrapper
    def clear(self):
        self.widget.delete('1.0', tk.END)

    @func_wrapper
    def _read_value(self):
        return self.widget.get(1.0, tk.END)

@class_wrapper
class formCombobox(_form_widget_base):

    def __init__(self, owner, val_tab, val_col, pop_tab, pop_col, tool_tip=None, **kw):
        super().__init__(owner, val_tab, val_col)
        self.logger.set_level(Logger.DEBUG)

        self.pop_tab = pop_tab
        self.pop_col = pop_col

        self.widget = ttk.Combobox(self, state='readonly', **kw)
        self.populate()
        self.widget.grid()
        self.widget.bind("<<ComboboxSelected>>", self._bind_key)
        if not tool_tip is None:
            self.tool_tip = toolTip(self, tool_tip)

    @func_wrapper
    def getter(self):
        value = self._read_value()
        self.data.write_single_value(self.table, self.column, self.row_id, value)

    @func_wrapper
    def setter(self):
        self.populate()
        value = self.data.read_single_value(self.table, self.column, self.row_id)
        # Bug Fix.
        # the value in the database can never be 0 or None. It has to be a row ID
        # of a table, which starts at 1. So, if we find a None or a 0 here, set it
        # to a reasonable default.
        if value is None or value == 0:
            self.data.write_single_value(self.table, self.column, self.row_id, 1)
            self.data.commit()
            self.widget.current(0)
        else:
            # add or subtract 1 to convert database value to widget index.
            self.widget.current(int(value)-1)

    @func_wrapper
    def clear(self):
        try:
            self.widget.current(0)
        except tk.TclError:
            pass # empty content is not an error

    @func_wrapper
    def populate(self):
        self.widget['values'] = self.data.get_column_list(self.pop_tab, self.pop_col)

    @func_wrapper
    def _read_value(self):
        val = self.widget.current()+1
        self.logger.debug('combo read value = %d'%(val))
        return val

@class_wrapper
class formDynamicLabel(_form_widget_base):

    def __init__(self, owner, table, column, tool_tip=None, **kw):
        super().__init__(owner, table, column)
        self.logger.set_level(Logger.DEBUG)

        self.value = tk.StringVar(self)
        self.widget = tk.Label(self, textvariable=self.value, **kw)
        self.widget.grid()
        if not tool_tip is None:
            self.tool_tip = toolTip(self, tool_tip)

    @func_wrapper
    def setter(self):
        value = self.data.read_single_value(self.table, self.column, self.row_id)
        if value is None:
            self.value.set('')
        else:
            self.value.set(str(value))

    @func_wrapper
    def getter(self):
        pass

    @func_wrapper
    def _read_value(self):
        pass

@class_wrapper
class formIndirectLabel(_form_widget_base):

    def __init__(self, owner, val_tab, val_col, rem_tab, rem_col, tool_tip=None, **kw):
        super().__init__(owner, val_tab, val_col)
        self.logger.set_level(Logger.DEBUG)

        self.rem_tab = rem_tab
        self.rem_col = rem_col

        self.value = tk.StringVar(self)
        self.widget = tk.Label(self, textvariable=self.value, **kw)
        self.widget.grid()
        if not tool_tip is None:
            self.tool_tip = toolTip(self, tool_tip)

    @func_wrapper
    def getter(self):
        # This is the name
        value = self.value.get()
        # find the row ID where the name matches in the rem_tab
        id = self._read_value()
        # set the value with the row_id
        self.data.write_single_value(self.table, self.column, self.row_id, id)

    @func_wrapper
    def setter(self):
        # this is the ID
        id = self.data.read_single_value(self.table, self.column, self.row_id)
        # find the value with the row ID in the table
        value = self.data.read_single_value(self.rem_tab, self.rem_col, id)
        # set the widget value
        self.value.set(str(value))

    @func_wrapper
    def clear(self):
        self.value.set('')

    # @func_wrapper
    # def _read_value(self):
    #     return self.data.get_row_id(self.rem_tab, self.rem_col, value)

@class_wrapper
class formTitle(_form_widget_base):

    def __init__(self, owner, value, **kw):
        super().__init__(owner, None, None)
        self.logger.set_level(Logger.DEBUG)

        self.widget = tk.Label(self, text=value, font=("Helvetica", 14), **kw)
        self.widget.grid()

@class_wrapper
class formCheckbox(_form_widget_base):

    def __init__(self, owner, table, column, tool_tip=None, **kw):
        super().__init_(owner, table, column)
        self.logger.set_level(Logger.DEBUG)

        self.value = tk.BooleanVar()
        self.widget = tk.Checkbutton(self, var=self.value, command=self._bind_key, **kw)
        self.widget.grid()
        if not tool_tip is None:
            self.tool_tip = toolTip(self, tool_tip)

    @func_wrapper
    def getter(self):
        val = self._read_value()
        self.data.write_single_value(self.table, self.column, self.row_id, val)

    @func_wrapper
    def setter(self):
        val = self.data.read_single_value(self.table, self.column, self.row_id)
        self.value.set(val)

    @func_wrapper
    def clear(self):
        self.value.set(0)

    @func_wrapper
    def _read_value(self):
        return self.int(self.value.get())

# Note that radio buttons are not represented in this library. I don't need them for the
# applications that I am writing because I use a combo box instead. They take up less
# room on the form.