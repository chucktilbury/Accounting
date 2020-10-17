import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from tkinter.messagebox import *
from system.database import Database
from widgets.form_widgets import toolTip
from system.logger import *

swtt = \
'''
Search for entry:
Type a few characters and the hit the down arrow
to see the list of current matches. Choose one and
select the "OK" button.
'''

@class_wrapper
class searchWidget(ttk.Combobox):
    '''
    This generates a list of items for a combo box. Placing characters in the combo
    generates a list using the "LIKE" SQL keyword and presents a sorted list.
    '''

    def __init__(self, owner, table, column, tool_tip=None, **kw):
        super().__init__(owner, **kw)
        self.logger.set_level(Logger.DEBUG)

        self.table = table
        self.column = column
        if not tool_tip is None:
            self.ttip = toolTip(self, tool_tip)

        self.bind('<KeyRelease>', self._key_handler)
        self.data = Database.get_instance()

        self._generate_list()

    def _key_handler(self, event=None):
        self._generate_list()

    def _generate_list(self):
        newkey = self.get() + '%'
        line = 'SELECT %s FROM %s WHERE %s LIKE \'%s\''%(self.column, self.table, self.column, newkey)

        cur = self.data.execute(line)
        lst = []

        try:
            for item in cur:
                lst.append(item[0])
        except Exception as e:
            self.logger.debug('searchWidget exception: %s'%(str(e)))

        lst.sort()
        self['values'] = lst

