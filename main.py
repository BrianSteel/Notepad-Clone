# GUI Notepad By Brian
# 17/06/2021

from tkinter import *
from tkinter.font import Font
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os

def tksetup(root): 
    # Adding title
    title = "Untitled - Notepad"
    root.title(title)
    # Setting icon
    root.iconbitmap("img/icon.ico")
    # Setting default size
    root.geometry("400x400")
    # Setting minimum size
    root.minsize(600, 500)
    global size
    global font
    font = Font(family = 'lucida', size = size)

    # create the components - menubar
    menuBar = createMenuBar(root)
    # create menubar file menu, edit menu, help menu, text area, status bar
    createFileMenu(menuBar, root)
    createEditMenu(menuBar)
    createViewMenu(menuBar, font)
    createHelpMenu(menuBar)
    createTextarea(root, font)
    createBtmStatusBar(root)
    # loop keeps tkinter window/s alive
    root.mainloop()


def createMenuBar(root):
    # Creating a Menu Bar 
    MenuBar = Menu(root)
    # configures the roots prebuilt menu config
    root.config(menu = MenuBar)
    return MenuBar

def createFileMenu(MenuBar, root):
    # File Menu
    FileMenu = Menu(MenuBar, tearoff = 0)
    # To open a New File
    FileMenu.add_command(label = "New", command = newFile)
    # To open already existing File
    FileMenu.add_command(label = "Open", command = openFile)
    # To save the current file
    FileMenu.add_command(label = "Save", command = lambda: saveFile(root.title()))
    # Open new window
    FileMenu.add_command(label = "New Window", command = newWindow)
    # To add a seperating line
    FileMenu.add_separator()
    # To quit the notepad
    FileMenu.add_command(label = "Exit", command = lambda: quitApp(root))
    # Add file menu to the menubar
    MenuBar.add_cascade(label = "File", menu = FileMenu)

def createEditMenu(MenuBar):
     # Edit Menu
    EditMenu = Menu(MenuBar, tearoff = 0)
    # To give a feature of Cut, Copy, Paste
    EditMenu.add_command(label = "Cut", command = cut)
    EditMenu.add_command(label = "Copy", command = copy)
    EditMenu.add_command(label = "Paste", command = paste)
    # Add edit menu to menubar
    MenuBar.add_cascade(label = "Edit", menu = EditMenu)

def createHelpMenu(MenuBar): 
    # Help Menu
    HelpMenu = Menu(MenuBar, tearoff = 0)
    # Info for Notepad
    HelpMenu.add_command(label = "About Notepad", command = about)
    # Add help menu to menubar
    MenuBar.add_cascade(label = "Help", menu = HelpMenu)

def createViewMenu(MenuBar, font): 
    ViewMenu = Menu(MenuBar, tearoff = 0)
    # Add Zoom In shortcut
    ViewMenu.add_command(label = 'Zoom In (Ctrl + Plus)', command = onZoomInTextArea)
    # Add Zoom out shortcut
    ViewMenu.add_command(label = 'Zoom Out (Ctrl + Minus)', command = onZoomOutTextArea)
    # revert to normal font size
    ViewMenu.add_command(label = 'Revert Font Size', command = onRevertFont)
    # Add view menu to menubar
    MenuBar.add_cascade(label = "View", menu = ViewMenu)

def createTextarea(root, font): 
     # Text area for writing text
    global TextArea 
    TextArea = Text(root, font = font)
    # Add shortcuts to text 
    TextArea.bind('<Control-plus>', onZoomInTextArea)
    TextArea.bind('<Control-minus>', onZoomOutTextArea)
    # an event is there so you must use it or your will get error
    TextArea.bind('<Control-s>', lambda event : saveFile(root.title()))
    TextArea.pack(expand = True, fill = BOTH)

    # Adding Scrollbar using rules from tkinter
    scroll = Scrollbar(TextArea)
    scroll.pack(side = RIGHT, fill = Y)
    scroll.config(command = TextArea.yview)
    TextArea.config(yscrollcommand = scroll.set)

def createBtmStatusBar(root): 
    # create status bar
    statusbar = Frame(root, bd=1, relief=SUNKEN) 
    statusbar.pack(side=BOTTOM, fill=X)
    # create labels on staus bar
    label1 = Label(statusbar, text="UTF-8", width=20)
    label1.pack(side = RIGHT)
    label2 = Label(statusbar, text="Windows(CRLF)", width=20)
    label2.pack(side=RIGHT)

def newFile():
    global file
    root.title("Untitled - Notepad")
    file = None
    TextArea.delete(1.0, END)

def onZoomInTextArea(*event):
    global size
    if size >= 150:
        return
    if event and event[0].keycode == 107:
        size = size + 5
    else:
        size = size + 1 
    font.config(size = size)

def onZoomOutTextArea(*event):
    global size
    if size <= 13:
        return
    if event and event[0].keycode == 109:
        size = size - 5
    else:
        size = size - 1 
    font.config(size = size)

def onRevertFont(): 
    global size
    size = 13
    font.config(size = size)

def newWindow(): 
    # creates new window
    # almost same as initiating tkinter
    # here it initiates new top-level window to root
    window = Toplevel(root)
    # window.lift()
    # window.attributes("-topmost", True)
    window.focus_set()
    tksetup(window)

def openFile():
    global file
    file = askopenfilename(defaultextension = ".txt", filetypes=[("All files", "*.*"), ("Text Documents", "*.txt")])

    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + "- Notepad")
        TextArea.delete(1.0, END)

        f = open(file, "r")
        TextArea.insert(1.0,f.read())

        f.close()

def saveFile(title):
    global file
    if file == None:
        print(title)
        file = asksaveasfilename(initialfile = title, defaultextension = ".txt", filetypes=[("All files", "*.*"), ("Text Documents", "*.txt")])

        if file == "":
            file = None

        else:
            #Save it as a New File
            f = open(file, "w")
            f.write(TextArea.get(1.0, END))
            f.close()

            root.title(os.path.basename(file) + " - Notepad")
    else:
        f = open(file, "w")
        f.write(TextArea.get(1.0, END))
        f.close()


def quitApp(root):
    print(root)
    root.destroy()


def cut():
    TextArea.event_generate(("<<Cut>>"))

def copy():
    TextArea.event_generate(("<<Copy>>"))

def paste():
    TextArea.event_generate(("<<Paste>>"))

def about():
    showinfo("About Notepad", "Notepad by Brian")


if __name__ == '__main__':
    TextArea = None
    file = None
    size = 13
    font = None
    # Creating an instance of tkinter
    root = Tk()
    tksetup(root)

    # Check pack() Frame() event_generate() 