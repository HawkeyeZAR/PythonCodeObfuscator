"""
PyFuscater is a source code obfuscater for python.

Created by Jack Ackermann
"""


from tkinter import Tk, ttk, Frame, FALSE, Button, Entry, StringVar,\
     messagebox,filedialog

import libs.tooltip as tt
from libs.obfuscator import Obfuscator


class PyFuscater(Frame):
    
    def centre_window(self):
        w = 600
        h = 75
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        centre_title = (' '*25)  # Use spaces to center Title
        title_txt = 'PyFuscater - A source code obfuscater for python scripts'
        self.root.title(centre_title + title_txt)
        self.centre_window()
        self.grid(column=0, row=0, sticky='nsew')

        self.file_name = ''   
        self.obf = Obfuscator(self.file_name)

        # Entry Widget Section
        self.file_entry_txt = StringVar()
        self.file_entry = ttk.Entry(self, textvariable=self.file_entry_txt,
                                    width=60, state='readonly')
        self.file_entry.grid(column=1, row=0, sticky='w', padx=10)
        self.file_entry.configure(font='Ariel 9')

        # Button Section
        self.open_btn = Button(self, text='Load File', command=self.open_file)
        self.open_btn.grid(column=0, row=0, sticky='w')
        self.open_btn.configure(width=9, font='Ariel 9 bold')

        self.obf_btn = Button(self, text='Obfuscate', command=self.do_obf)
        self.obf_btn.grid(column=0, row=1, sticky='w')
        self.obf_btn.configure(width=9, font='Ariel 9 bold', state='disabled')

        self.del_btn = Button(self, text='Delete Lines', command=self.del_lines)
        self.del_btn.grid(column=1, row=1, sticky='w', padx=10)
        self.del_btn.configure(width=10, font='Ariel 9 bold', state='disabled')

        self.doc_btn = Button(self, text='Delete Comments',
                              command=self.del_comments)
        self.doc_btn.grid(column=1, row=1, sticky='w', padx=100)
        self.doc_btn.configure(width=15, font='Ariel 9 bold', state='disabled')

        self.exit_btn = Button(self, text='Exit', command=self.on_exit)
        self.exit_btn.grid(column=2, row=0, sticky='w')
        self.exit_btn.configure(width=7, font='Ariel 9 bold')

        # Create tool tips for widgets
        tt_text1 = 'Obfuscate all user defined names for classes and functions'
        tt_text2 = 'Delete all blank lines inside the python source code'
        tt.create_tooltip(self.obf_btn, tt_text1)
        tt.create_tooltip(self.del_btn, tt_text2)

        # Place padding around frames, to improve look and feel
        for child in self.root.winfo_children():
            child.grid_configure(padx=10, pady=10)


    # Button Callback events go here
    def open_file(self):
        try:
            file_type = [("All Files","*.*")]
            title_text = "---- Please select the file to edit ----"
            file = filedialog.askopenfilename(filetypes=file_type,
                                                   title=title_text)
        except:
            messagebox.showerror("File Error", "File could not be opened")
        else:
            self.file_entry_txt.set(file)
            self.file_name = self.file_entry_txt.get()
            self.obf_btn.configure(state='normal')
            self.del_btn.configure(state='normal')
            self.doc_btn.configure(state='normal')

    def do_obf(self): # calls obf_data function in obfuscator.py
        self.obf.obf_data(self.file_name)

    def del_lines(self): # calls del_blank_lines() function in obfuscator.py
        self.obf.del_blank_lines(self.file_name)

    def del_comments(self): # calls del_doc_str() function in obfuscator.py
        self.obf.del_doc_str(self.file_name)
    
    def on_exit(self):
        self.root.destroy()


def main():
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    # root.configure(background="black")
    PyFuscater(root)
    root.mainloop()

if __name__ == '__main__':
    main()
