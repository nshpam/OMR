from tkinter import *
from tkinter import ttk

def CustomAnswer():
    MenuWindow.goto_custom_ans()
    print('--- Custom Answer Page ---')

def ImportPDF():
    
    PDFWindow = PDFWin(MenuWindow.goto_import_pdf(),'Import PDF Window')
    PDFWindow.label('test')
    print('--- Import PDF Page ---')

class Window:
    def __init__(self, win, WinTitle):
        self.win = win
        win.title(WinTitle)
        win.geometry("250x100")

    def label(self,LabelWin, LabelText):
        self.CustomLabel = Label(LabelWin, text=LabelText)
        self.CustomLabel.pack()
    
    def button(self, GUIWin, ButtonText, ButtonCommand):
        self.CustomButton = Button(GUIWin, text=ButtonText, command=ButtonCommand)
        self.CustomButton.pack()
    
    def goto_custom_ans(self):
        self.goto_custom_ans = Toplevel(self.win)
        CustomAnsWin(self.goto_custom_ans,'Custom Answer Window')
        self.win.withdraw()

    def goto_import_pdf(self):
        self.goto_import_pdf = Toplevel(self.win)
        
        self.win.withdraw()

class CustomAnsWin:
    def __init__(self, win, WinTitle):
        self.win = win
        win.title(WinTitle)
        win.geometry("250x100")

    def label(self,LabelWin, LabelText):
        self.CustomLabel = Label(LabelWin, text=LabelText)
        self.CustomLabel.pack()
    
    def button(self, GUIWin, ButtonText, ButtonCommand):
        self.CustomButton = Button(GUIWin, text=ButtonText, command=ButtonCommand)
        self.CustomButton.pack()

class PDFWin:
    def __init__(self, win, WinTitle):
        self.win = win
        win.title(WinTitle)
        win.geometry("250x100")

    def label(self,LabelWin, LabelText):
        self.CustomLabel = Label(LabelWin, text=LabelText)
        self.CustomLabel.pack()
    
    def button(self, GUIWin, ButtonText, ButtonCommand):
        self.CustomButton = Button(GUIWin, text=ButtonText, command=ButtonCommand)
        self.CustomButton.pack()


#main program
MainMenu = Tk()
MenuWindow = Window(MainMenu,'MainMenu')
MenuWindow.label(MainMenu,'Select your method')
MenuWindow.button(MainMenu,'Custom Answer',CustomAnswer)
MenuWindow.button(MainMenu,'Import PDF',ImportPDF)

MainMenu.mainloop()