
import tkinter as tk
import tkinter.ttk as ttk
from database import Database
from search_widget import searchWidget

class SelectDialog(tk.Toplevel):

    def __init__(self, owner, table, column, thing=None):
        super().__init__(owner)

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

    def _ok_btn(self):
        id = self.data.get_id_by_column(self.table, self.column, self.cbb.get())
        self.item_id = id
        self.destroy()

    def _cancel_btn(self):
        self.destroy()