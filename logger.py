
import sys, time
import tkinter as tk
from tkinter.messagebox import showerror
from tkinter.filedialog import asksaveasfilename as get_filename
#import logging

class _logger(tk.Toplevel): #(tk.Frame):
    '''
    This class is the base class that has the TK window that the logs go into. It is
    not intended to be inherited or used stand-alone. It is used by the Logger class
    to display the logs.
    '''
    _instance = None

    @staticmethod
    def get_instance():
        '''
        This class is a singleton. All classes using this should call get_instance(),
        rather than instantiating it directly.
        '''
        if _logger._instance is None:
            _logger()
        return _logger._instance

    def __init__(self):

        if _logger._instance is None:
            _logger._instance = self
        else:
            raise Exception("Logger class is a singleton. Use get_instance() instead.")

        super().__init__(None)
        self.title('Logger Window')
        self.resizable(0, 0)

        self.win_frame = tk.Frame(self)
        self.text_frame = tk.Frame(self.win_frame, bd=1, relief=tk.RIDGE)

        self.text = tk.Text(self.text_frame, wrap=tk.NONE, state='disabled', width=162, height=50)
        self.text.configure(font='TkFixedFont')
        #self.text.grid(row=0, column=0, columnspan=3, sticky='nw')

        self.vsb = tk.Scrollbar(self.text_frame, orient='vertical')
        self.vsb.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.vsb.set)
        #self.vsb.grid(row=0, column=1, sticky='nse')#'nws')
        self.vsb.pack(side='right', fill='y')

        self.hsb = tk.Scrollbar(self.text_frame, orient='horizontal')
        self.hsb.config(command=self.text.xview)
        self.text.config(xscrollcommand=self.hsb.set)
        #self.hsb.grid(row=1, column=0, sticky='ews')#'ewn')
        self.hsb.pack(side='bottom', fill='x')
        self.text.pack(side='top', fill='both', expand=True)

        self.text_frame.grid(row=0, column=0, columnspan=3)#, sticky='w')


        tk.Button(self.win_frame, text='Save', width=15, command=self.save_cb).grid(row=1, column=0, sticky='e', padx=5)
        tk.Button(self.win_frame, text='Clear', width=15, command=self.clear_cb).grid(row=1, column=1, padx=5)
        tk.Button(self.win_frame, text='Hide', width=15, command=self.cancel_cb).grid(row=1, column=2, sticky='w', padx=5)

        self.win_frame.grid()

        self.withdraw() # hidden by default
        self.enabled = False

    def destroy(self):
        '''
        Override the parent to prevent this from being destroyed with the system menu.
        '''
        self.disable()

    def toggle(self):
        '''
        Toggle visibility.
        '''
        if self.enabled:
            self.disable()
        else:
            self.enable()

    def enable(self):
        '''
        Show the logging window.
        '''
        self.update()
        self.deiconify()
        self.enabled = True

    def disable(self):
        '''
        Hide the logging window.
        '''
        self.withdraw()
        self.enabled = False

    def write(self, msg):
        '''
        Add the message to the scrolling text control.
        '''
        self.text.configure(state='normal')
        self.text.insert(tk.END, msg)
        self.text.configure(state='disabled')
        self.text.yview(tk.END) # Autoscroll to the bottom

    def save_cb(self):
        '''
        Save button callback.
        '''
        result = get_filename(initialdir='.', title='Save Log File', filetypes=(('text files', '*.txt'), ('all files', '*')))
        txt = self.text.get(1.0, tk.END)
        with open(result, 'w') as fh:
            fh.write(txt)

    def clear_cb(self):
        '''
        Clear button callback.
        '''
        self.text.configure(state='normal')
        self.text.delete('1.0', tk.END)
        self.text.configure(state='disabled')

    def cancel_cb(self):
        '''
        Cancel button callback. Stops logging, hides the window.
        '''
        self.disable()
        self.enabled = False


class Logger:
    '''
    Logger class produces messages on the text console. Used mostly for
    debugging. Supports individual class debugging and debug levels.
    '''

    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    MESSAGE = 4

    def __init__(self, name, level=MESSAGE):
        '''
        Instantiate this class for each class that will use the logging
        functionality.
        '''

        # for comparison to the requested level
        self.dbg = 0
        self.inf = 1
        self.warn = 2
        self.err = 3
        self.mess = 4

        # if the name is a string, then use it, else if it's an object, then
        # use its name.
        if type(name) == str:
            self.name = name
        else:
            self.name = name.__class__.__name__

        # level stack
        self.level = []
        self.level.insert(0, level)

        # set the output location
        self.stream = _logger.get_instance()
        self.enabled = self.stream.enabled

    def toggle_visibility(self):
        '''
        This must be called exactly one time to facilitate enabling and disabling
        the window. It must be called before any text is written to the logger.
        '''
        self.stream.toggle()

    def fmt(self, args, lev):
        '''
        Format the value to be printed.
        '''
        t = time.strftime("[%Y%m%d %H:%M:%S]")
        return "%s %s: %s: %s\n"%(t, lev, self.name, args)

    def debug(self, args, frame_num = 1):
        '''
        Print a debug message.
        '''
        if self.level[0] <= self.dbg:
            s1 = sys._getframe(frame_num).f_code.co_name
            t = time.strftime("[%Y%m%d %H:%M:%S]")
            self.stream.write("%s %s: %s.%s(): %s\n"%(t, "DEBUG", self.name, s1, args))

    def info(self, args):
        '''
        Print an info message.
        '''
        if self.level[0] <= self.inf:
            self.stream.write(self.fmt(args, 'INFO'))

    def warning(self, args):
        '''
        Print a wanring message.
        '''
        if self.level[0] <= self.warn:
            self.stream.write(self.fmt(args, 'WARNING'))

    def error(self, args):
        '''
        Print an error message and show a dialog. These messages are always enabled,
        regardless of the logging level. When the OK button is hit on the dialog,
        the program continues.
        '''
        val = self.fmt(args, 'ERROR')
        self.stream.write(val)
        showerror("ERROR", val)


    def msg(self, args):
        '''
        Print a normal message.
        '''
        if self.level[0] <= self.mess:
            self.stream.write(self.fmt(args, 'MSG'))

    def fatal(self, args):
        '''
        Log a fatal error message and show an error dialog. When the OK button is
        pressed on the dialog, the program is terminated.
        '''
        val = self.fmt(args, 'FATAL ERROR')
        self.stream.write(val)
        self.stream.write("System cannot continue\n\n")
        showerror('FATAL ERROR', val)
        sys.exit(1)

    def push_level(self, level):
        '''
        Push a debug level on the stack. This can be used to temperarilly enable or disable
        messages od a certin level.
        '''
        self.level.insert(0, level)

    def pop_level(self):
        '''
        Restores the logging level after a value has been pushed on to it.
        '''
        if len(self.level) > 1:
            self.level.remove(0)

    def set_level(self, level):
        '''
        Set the current logging level.
        '''
        self.level[0] = level

    def debugger(self, name, args):
        '''
        This is used in the @debugger decorator to print messages.
        '''
        if self.level[0] <= self.dbg:
            t = time.strftime("[%Y%m%d %H:%M:%S]")
            self.stream.write("%s %s: %s.%s(): %s\n"%(t, "DEBUG", self.name, name, args))

def func_wrapper(func):
    '''
    This is a decorator used to decorate methods on a class for debugging.
    '''
    def wrapper(*args, **kw):

        args[0].logger.debugger(func.__name__, '--enter: %s %s'%(str(args), str(kw)))
        retv = func(*args, **kw)
        args[0].logger.debugger(func.__name__, '--returning: %s'%(str(retv)))

        return retv

    return wrapper

def class_wrapper(cl):
    '''
    This decorator is for classes. It creates the logger and decorates the __init__
    function by monkey patching it.
    '''
    orig_init = cl.__init__
    def new_init(self, *args, **kw):
        self.logger = Logger(self)
        self.logger.debugger('__init__', '-- enter %s %s'%(args, kw))
        orig_init(self, *args, **kw)
        self.logger.debugger('__init__', '-- returning')

    cl.__init__ = new_init
    return cl

