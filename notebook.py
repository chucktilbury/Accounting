import tkinter as tk
import tkinter.ttk as ttk
from logger import *

@class_wrapper
class Notebook(tk.Frame):
    '''
    Notebook widget
    '''

    def __init__(self, owner, tabs=None, **kw):
        '''
        Construct the notebook widget.

        owner   =   The frame to which this notebook belongs.
        tabs    =   List of tabs to create.
        **kw    =   Named args passed to the frame.
        '''
        super().__init__(owner, **kw)

        self.owner = owner
        self.frame_list = []
        self.frame_index = 0
        self.crnt_index = 0
        self.btn_width = 10

        self.btn_frame = tk.LabelFrame(self)
        self.btn_frame.grid(row=0, column=0, pady=5, sticky='nw')

        if not tabs is None:
            for item in tabs:
                self.add_tab(item)

        self.grid()

    @func_wrapper
    def add_tab(self, name, show_cb=None, hide_cb=None):
        '''
        Add a tab to the notebook with the specified name. Creates a frame for the
        tab and places it in the list, but does not display it.
        '''
        frame = tk.Frame(self)
        button = tk.Button(self.btn_frame, text=name, width=self.btn_width, relief='raised',
                            command=lambda idx=self.frame_index: self.show_tab(idx) )
        button.grid(row=0, column=self.frame_index, sticky='w')

        self.frame_list.append({'name':name,
                                'frame':frame,
                                'button':button,
                                'show_cb':show_cb,
                                'hide_cb':hide_cb})
        self.frame_index += 1

    @func_wrapper
    def show_tab(self, index):
        '''
        Hide the previously displayed tab and replace it with the new one.
        '''
        self.frame_list[self.crnt_index]['frame'].grid_forget()
        self.frame_list[self.crnt_index]['button'].configure(relief='raised')
        if not self.frame_list[self.crnt_index]['hide_cb'] is None:
            self.frame_list[self.crnt_index]['hide_cb']()

        self.frame_list[index]['frame'].grid(row=1, column=0, sticky='sw')
        self.frame_list[index]['button'].configure(relief='sunken')
        if not self.frame_list[index]['show_cb'] is None:
            self.frame_list[index]['show_cb']()

        self.crnt_index = index

    @func_wrapper
    def get_frame(self, index):
        '''
        Return the frame of the tab at the index.
        '''
        return self.frame_list[index]['frame']

    @func_wrapper
    def get_tab_index(self, name):
        '''
        Return the index of a tab given the name.
        '''
        for idx, item in enumerate(self.frame_list):
            if item['name'] == name:
                return idx

        return -1   # not found

