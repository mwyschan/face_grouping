from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import cv2
import tkinter.font as font
import os
from os import listdir
from PIL import Image, ImageTk
import numpy as np
import logic2
import threading
import shutil   

window = Tk()
window.title("GUH")
window.geometry("900x600")
window.resizable(width=False, height=False)
window.configure(bg="#000000")

def status_bar(custom, colour):
    statusFrame = Frame(window, width=900, height=30, bd=2, relief=SUNKEN, bg="#9932CC")
    statusFrame.pack_propagate(False)
    statusLabel = Label(statusFrame, text=custom, fg=colour, bg="#9932CC")
    statusLabel.place(anchor=W, rely=0.5)
    statusFrame.place(anchor=W, rely=0.975)
    window.update()

def fix_folder():
    global dirVar
    global sortedDir
    global selectedfile
    global globalflag
    selected_path = filedialog.askdirectory(initialdir=os.path.dirname(dirVar))
    shutil.move(sortedDir + "/" + selectedfile, selected_path)
    globalflag = False
    status_bar("Fix completed.", "#3FB8F4")

# def rename():
#     rename_window = Toplevel(window)
#     rename_window.geometry("400x300")
#     rename_window.resizable(width=False, height=False)
#     filelisting = Listbox(rename_window, height=20, width=40, selectmode=SINGLE)
#     filelisting.place(anchor=W, relx=0.02, rely=0.5)
#     for i in listdir(sortedDir):
#         if i.endswith("png") or i.endswith("jpg") or i.endswith("jpeg"):
#             filelisting.insert(END, i)   
#     if filelisting.size() == 0:
#         messagebox.showerror("Folder Empty", "Folder GUHProject is empty.\nPlease add images into the folder.")
#         fileselect_window.destroy()
#     imagelabelframe = Frame(fileselect_window, width=620, height=550, bd=2, relief=SUNKEN)
#     imagelabelframe.pack_propagate(False)
#     imagelabel = Label(imagelabelframe, anchor=CENTER)
#     imagelabelframe.place(relx=0.99, rely=0.015, anchor=NE)
#     imagelabel.place(relx=0.5, rely=0.5, anchor=CENTER)
#     fix = Button(fileselect_window, text="Fix", width=8, height=1, bd=2, command=fix_folder)
#     fix.place(relx=0.99, rely=0.99, anchor=SE)
#     currentindex = []
#     while globalflag:
#         selectedfileindex = list(filelisting.curselection())
#         fileselect_window.update()
#         if selectedfileindex == currentindex:
#             continue
#         elif selectedfileindex != []:
#             global selectedfile
#             selectedfile = filelisting.get(selectedfileindex)
#             print(selectedfile)
#             selectedimage = cv2.imread(sortedDir + "/" + selectedfile)
#             b,g,r = cv2.split(selectedimage)
#             imagergb = cv2.merge((r,g,b))
#             imagergb_obj = Image.fromarray(imagergb)
#             x = imagergb_obj.size[0]
#             y = imagergb_obj.size[1]
#             ratio = min(600 / x, 530 / y) #620x550, slightly smaller to fit frame
#             if x > 600 or y > 530:
#                 x = int(x * ratio)
#                 y = int(y * ratio)
#             imagergb_obj = imagergb_obj.resize((x, y), Image.ANTIALIAS)
#             imagergb_tk = ImageTk.PhotoImage(image=imagergb_obj)
#             imagelabel.configure(image=imagergb_tk)
#             currentindex = selectedfileindex
#     display = Label(rename_window, text= "What do you want this file as?").place(x=10, y=20)
#     e = Entry(rename_window)
#     e.place(x=40, y=20)
#     s = e.get()
#     print(s)

def create_fileselect():
    global dirVar
    global sortedDir
    global globalflag
    sortedDir = filedialog.askdirectory(initialdir=os.path.dirname(dirVar))
    fileselect_window = Toplevel(window)
    fileselect_window.geometry("900x600")
    fileselect_window.resizable(width=False, height=False)

    filelisting = Listbox(fileselect_window, height=36, width=40, selectmode=SINGLE)
    filelisting.place(anchor=W, relx=0.02, rely=0.5)
    for i in listdir(sortedDir):
        if i.endswith("png") or i.endswith("jpg") or i.endswith("jpeg"):
            filelisting.insert(END, i)   
    if filelisting.size() == 0:
        messagebox.showerror("Folder Empty", "Folder GUHProject is empty.\nPlease add images into the folder.")
        fileselect_window.destroy()
    imagelabelframe = Frame(fileselect_window, width=620, height=550, bd=2, relief=SUNKEN)
    imagelabelframe.pack_propagate(False)
    imagelabel = Label(imagelabelframe, anchor=CENTER)
    imagelabelframe.place(relx=0.99, rely=0.015, anchor=NE)
    imagelabel.place(relx=0.5, rely=0.5, anchor=CENTER)
    fix = Button(fileselect_window, text="Fix", width=8, height=1, bd=2, command=fix_folder)
    fix.place(relx=0.99, rely=0.99, anchor=SE)
    currentindex = []
    while globalflag:
        selectedfileindex = list(filelisting.curselection())
        fileselect_window.update()
        if selectedfileindex == currentindex:
            continue
        elif selectedfileindex != []:
            global selectedfile
            selectedfile = filelisting.get(selectedfileindex)
            print(selectedfile)
            selectedimage = cv2.imread(sortedDir + "/" + selectedfile)
            b,g,r = cv2.split(selectedimage)
            imagergb = cv2.merge((r,g,b))
            imagergb_obj = Image.fromarray(imagergb)
            x = imagergb_obj.size[0]
            y = imagergb_obj.size[1]
            ratio = min(600 / x, 530 / y) #620x550, slightly smaller to fit frame
            if x > 600 or y > 530:
                x = int(x * ratio)
                y = int(y * ratio)
            imagergb_obj = imagergb_obj.resize((x, y), Image.ANTIALIAS)
            imagergb_tk = ImageTk.PhotoImage(image=imagergb_obj)
            imagelabel.configure(image=imagergb_tk)
            currentindex = selectedfileindex
    fileselect_window.destroy()
    globalflag = True

def create_about():
    messagebox.showinfo("About", "GUH 2019\n\nVersion 1.0")

def back_end():
    global dirVar
    if os.listdir(dirVar) == []:
        messagebox.showerror("Folder Empty", "Folder GUHProject is empty.\nPlease add images into the folder.")
        return
    status_bar("Processing...", "orange")
    facecheckthread = threading.Thread(target=logic2.backendlogic, args=(dirVar,))
    facecheckthread.start()
    flag = True
    while flag:
        if facecheckthread.isAlive() == False:
            status_bar("Done.", "#3FB8F4")
            flag = False

def create_button():
    global dirVar
    helv12 = font.Font(family='Helvetica', size=12, weight=font.BOLD)
    helv36 = font.Font(family='Helvetica', size=36, weight=font.BOLD) #the font of the plus sign 
    scan = Button(window, text= "Scan",font= helv36, width= 20, height= 5, bd=2, bg="#959DA5", command=back_end)
    scan.place(relx=0.5, rely=0.1, anchor=N) #placing the the add button at the top 
    view = Button(window, text="View/Fix", width=10, height=2, bd=2, font= helv12, bg="#959DA5", command=create_fileselect)
    view.place(relx=0.2, rely=0.75, anchor=N)
    open_folder = Button(window, text="Open Folder", width=10, height=2, bd=2, font=helv12, bg="#959DA5", command= lambda: os.startfile("C:" + dirVar))
    open_folder.place(relx= 0.5, rely=0.75, anchor=N)
    about = Button(window, text="About", width=10, height=2, bd=2, font= helv12, bg="#959DA5", command=create_about)
    about.place(relx=0.8, rely=0.75, anchor=N)

dirVar = "/Users/" + str(os.getlogin()) + "/Desktop/GUHProject/"
sortedDir = ""
selectedfile = ""
globalflag = True

create_button()
try:
    os.mkdir(dirVar)
    messagebox.showwarning("Folder Created", "Folder GUHProject has been created on the Desktop.\nPlease copy photos into the folder before scan.")
except:
    pass
status_bar("Ready.", "#00FF00")

window.mainloop()
