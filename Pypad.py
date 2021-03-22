from tkinter import *
from tkinter import filedialog,messagebox
import os,sys
import win32print
import win32api
class Pypad:
        #checking for the status of the file
    current_file="no-file"

    #command for new funtion to clear the area.
    def clear(self):
        self.area.delete(1.0,END)

    #commands defined below
        #new file
    def new_file(self,event=""):
        val = self.area.get(1.0,END)
        if not val.strip():
            pass
        else:
            res = messagebox.askyesnocancel("Save Dialog box","Do you want to save this file?")
            if res == True:
                self.saveas_file()
                self.clear()
            elif res == False:
                self.clear()

        # opening a file
    def open_file(self,event=""):
        res=filedialog.askopenfile(initialdir="/",title="Open",filetypes=(("Text Documents","*.txt"),("All Files","*.*")))
        val = self.area.get(1.0,END)
        if not val.strip():
            for i in res:
                self.area.insert(INSERT,i)
                self.current_file=res.name
        else:
            self.clear()
            for i in res:
                self.area.insert(INSERT,i)
                self.current_file=res.name

       #saving a file 
    def save_file(self,event=""):
        if self.current_file=="no-file":
            self.saveas_file()
        else:
            f=open(self.current_file,mode="w")
            f.write(self.area.get(1.0,END))
            f.close()

        #save as file
    def saveas_file(self,event=""):
        files=[("Text Document","*.txt"),("All files","*.*")]
        f=filedialog.asksaveasfile(mode="w",filetypes=files,defaultextension=files)
        data=self.area.get(1.0,END)
        f.write(data)
        self.current_file=f.name
        f.close()

        #printing a file via printer
    def print_file(self,event=""):
        printer_name=win32print.GetDefaultPrinter()
        file_print=filedialog.askopenfile(initialdir="/",title="Open",filetypes=(("Text Documents","*.txt"),("All Files","*.*")))
        if file_print:
            win32api.ShellExecute(0,"print",file_print,None,".",0)

        #exiting a file
    def exit_file(self):
        val = self.area.get(1.0,END)
        if not val.strip():
            quit()
        else:
            res = messagebox.askyesnocancel("Save Dialog box","Do you want to save this file?")
            if res == True:
                self.saveas_file()
                quit()
            elif res == False:
                quit()
        
        #undo command
    def undo_file(self,event=""):
        self.area.edit_undo()

        #redo command
    def redo_file(self,event=""):
        self.area.edit_redo()


        #cut command
    def cut_file(self,event=""):
        self.copy_file()
        self.area.delete('sel.first','sel.last')

        #copy command
    def copy_file(self,event=""):
        self.area.clipboard_clear()
        self.area.clipboard_append(self.area.selection_get())
    
        #paste command
    def paste_file(self,event=""):
        self.area.insert(INSERT,self.area.clipboard_get())

        #delete command
    def delete_file(self,event=""):
        self.area.delete('sel.first','sel.last')
        


    def __init__(self,master):
        self.master=master
        master.title("Pypad")
        master.iconbitmap(r'J:\DEVS\CODES\alternatives_opt\notepad\icon\icon.ico')
        master.bind("<Control-n>",self.new_file) #binding the command with a key for new file
        master.bind("<Control-o>",self.open_file) #binding the command with a key for opening
        master.bind("<Control-s>",self.save_file) #binding the command with a key for saving
        master.bind("<Control-Shift-S>",self.saveas_file) #binding the command with a key for save as
        master.bind("<Control-p>",self.print_file) #binding the command with a key for printing
        master.bind("<Control-Shift-Z>",self.undo_file) #binding the command with a key for undo
        master.bind("<Control-Shift-Y>",self.redo_file) #binding the command with a key for undo
        master.bind("<Control-Shift-X>",self.cut_file) #binding the command with a key for cut
        master.bind("<Control-Shift-C>",self.copy_file) #binding the command with a key for coping
        master.bind("<Control-Shift-V>",self.paste_file) #binding the command with a key for pasting
        master.bind("<Delete>",self.delete_file) #binding the command with a key for deleting
        self.area=Text(master,padx=5,pady=5,wrap=WORD,selectbackground="black",bd=2,insertwidth=2,undo=TRUE,autoseparators=True)
        self.area.pack(fill=BOTH,expand=1)
        self.main_menu=Menu()
        self.master.config(menu=self.main_menu)


        #menu bar for file
        self.file_menu=Menu(self.main_menu,tearoff=False)
        self.main_menu.add_cascade(label="File",menu=self.file_menu)
        self.file_menu.add_command(label="New", accelerator="Ctrl+N",command=self.new_file)
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O",command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S",command=self.save_file)
        self.file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S",command=self.saveas_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Print", accelerator="Ctrl+P",command=self.print_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit",command=self.exit_file)

        #menu bar for edit
        self.edit_menu=Menu(self.main_menu,tearoff=False)
        self.main_menu.add_cascade(label="Edit",menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", accelerator="Ctrl+Shift+Z",command=self.undo_file)
        self.edit_menu.add_command(label="Redo", accelerator="Ctrl+Shift+Y",command=self.redo_file)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+Shift+X",command=self.cut_file) 
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+Shift+C",command=self.copy_file)
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+Shift+V",command=self.paste_file)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Delete", accelerator="Del",command=self.delete_file)







root=Tk()
a=Pypad(root)
root.mainloop()
