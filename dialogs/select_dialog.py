
import tkinter as tk
import tkinter.ttk as ttk
from system.database import Database
from widgets.search_widget import searchWidget
from system.logger import *

@class_wrapper
class SelectDialog(tk.Toplevel):
    '''
    This class presents a simple select functionality on a single database
    column. It returns the row ID of the item that was selected. This dialog
    does not use the forms library for simplicity.
    '''

    def __init__(self, owner, table, column, thing=None):
        super().__init__(owner)
        self.logger.set_level(Logger.DEBUG)

        self.table = table
        self.column = column

        if thing is None:
            self.title('Select Item')
        else:
            self.title('Select %s'%(thing))

        self.data = Database.get_instance()

        self.item_id = -1   # impossible value

        self.upper_frame = tk.Frame(self)
        self.upper_frame.grid(row=0, column=0)
        self.lower_frame = tk.Frame(self)
        self.lower_frame.grid(row=1, column=0)

        tk.Label(self.upper_frame, text="Select %s"%(thing),
                        font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2)

        tk.Label(self.upper_frame, text='%s:'%(thing)).grid(row=1, column=0)
        self.cbb = searchWidget(self.upper_frame, table, column)
        self.cbb.grid(row=1, column=1, padx=5, pady=5)

        w = tk.Button(self.lower_frame, text="OK", width=10, command=self._ok_btn)
        w.grid(row=0, column=0, sticky='e')
        w = tk.Button(self.lower_frame, text="Cancel", width=10, command=self._cancel_btn)
        w.grid(row=0, column=1, sticky='w')
        self.wait_window(self)

    @func_wrapper
    def _ok_btn(self):
        id = self.data.get_id_by_column(self.table, self.column, self.cbb.get())
        self.item_id = id
        self.destroy()

    @func_wrapper
    def _cancel_btn(self):
        self.destroy()

@class_wrapper
class IndirectSelectDialog(SelectDialog):
    '''
    This class augments the select dialog so that the tables passed to it
    can be a forign key instead of a simple list. The value returned in
    self.item_id is a id of the row that contains the forign key.
    '''

    def __init__(self, owner, loc_tab, loc_col, for_tab, for_col, thing=None):
        self.logger.set_level(Logger.DEBUG)

        self.loc_tab = loc_tab
        self.loc_col = loc_col

        super().__init__(owner, for_tab, for_col, thing)

    @func_wrapper
    def _ok_btn(self):
        id = self.data.get_id_by_column(self.table, self.column, self.cbb.get())
        if id is None:
            # the value is not connected to a row.
            self.item_id = None
        else:
            self.item_id = self.data.get_row_id(self.loc_tab, self.loc_col, id)

        self.destroy()
