import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from tkinter.messagebox import *
from database import Database
from form_widgets import toolTip

swtt = \
'''
Search for entry:
Type a few characters and the hit the down arrow
to see the list of current matches. Choose one and
select the "OK" button.
'''

class searchWidget(ttk.Combobox):

    def __init__(self, owner, table, column, tool_tip=swtt, **kw):
        super().__init__(owner, **kw)

        self.table = table
        self.column = column
        if not tool_tip is None:
            self.ttip = toolTip(self, tool_tip)

        self.bind('<KeyRelease>', self._key_handler)
        self.data = Database.get_instance()

        self._generate_list()

    def _key_handler(self, event=None):
        #print(event, self.get())
        self._generate_list()

    def _generate_list(self):
        newkey = self.get() + '%'
        line = 'SELECT %s FROM %s WHERE %s LIKE \'%s\''%(self.column, self.table, self.column, newkey)

        cur = self.data.execute(line)
        lst = []

        try:
            for item in cur:
                lst.append(item[0])
        except:
            #print('exception')
            pass

        lst.sort()
        #print(lst)
        self['values'] = lst
        #self.set(lst[0])
