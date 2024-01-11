from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class MainWindow(ttk.Frame):
    ttk.Frame.__init__
    def __init__(self, root, title):
        self.parent = root
        self.title = title
        self.parent.geometry("250x100")
        self.parent.title(title)
        root.protocol("WM_DELETE_WINDOW", self.parent.destroy)
        
        label1 = ttk.Label(
            self.parent,
            text='Select your method')
        label1.pack()
        
        customans = ttk.Button(
            self.parent,
            text='Custom Answers',
            command=self.customansbtn)
        customans.pack()

        pdfans = ttk.Button(
            self.parent,
            text='PDF Answers',
            command=self.pdfansbtn
        )
        pdfans.pack()

    
    def customansbtn(self):
        customanswindow = Toplevel(self.parent)
        custom = CustomAnswer(customanswindow,'Custom Answers')
        

    def pdfansbtn(self):
        pdfanswindow = Toplevel(self.parent)
        custom = PDFAnswer(pdfanswindow,'PDF Answers')
        

    

class CustomAnswer(MainWindow):
    def __init__(self, root, title):
        self.parent = root
        self.title = title
        self.parent.geometry("200x150")
        self.parent.title(title)
        self.items = 1
        self.choices = 4
        root.protocol("WM_DELETE_WINDOW", self.onclosing) 
        
        ttk.Label(
            master=self.parent,
            text='Items'
        ).pack()
        
        self.entry1 = ttk.Entry(
            master=self.parent,
            textvariable=self.items
        )
        self.entry1.pack()

        ttk.Label(
            master=self.parent,
            text='Choices'
        ).pack()

        self.entry2 = ttk.Entry(
            master=self.parent,
            textvariable=self.choices
        )
        self.entry2.pack()
        
        ttk.Button(
            master=self.parent,
            text='Build Sheet',
            command=self.buildsheet
        ).pack()

    def buildsheet(self):
        sheetwindow = Toplevel(self.parent)
        self.items = self.entry1.get()
        self.choices = self.entry2.get()
        if len(self.items)==0 or len(self.choices)==0:
            self.items= '1'
            self.choices= '4'
        else:
            BuiltSheet(sheetwindow,'Sheet',self.items,self.choices)
            
        self.parent.withdraw()

    def onclosing(self):
        self.parent.destroy()
        

class PDFAnswer(MainWindow):
    def __init__(self, root, title):
        
        self.parent = root
        self.title = title
        self.parent.geometry("250x100")
        self.parent.title(title)

class BuiltSheet(MainWindow):
    def __init__(self, root, title,items,choices):
        #super().__init__(root, title)
        self.parent = root
        self.title = title
        self.items = int(items)
        self.choices = int(choices)
        self.height = 22*self.items+15
        self.width = 40*self.choices+100
        self.parent.geometry(str(self.width)+'x'+str(self.height))
        self.parent.title(title)
        
        self.answers = [StringVar() for i in range(self.items)]
        print(len(self.answers))
        self.buttonvals = [str(i+1) for i in range(self.choices)]
        for i in range(self.items):
            frame = ttk.Frame(
                self.parent
            )
            
            ttk.Label(
                frame,
                text=str(int(i)+1)
            ).pack(side='left')
            
            for j in range(self.choices):
                    ttk.Radiobutton(
                        frame,
                        value=str(i+1)+self.buttonvals[j],
                        variable=self.answers[i]
                    ).pack(side='left',padx=10)
            frame.pack(side='top')
        
        frame2 = ttk.Frame(self.parent)
        ttk.Button(
            frame2,
            text='Print answers',
            command= self.showans
        ).pack()
        frame2.pack()

    def showans(self):
        try:
            ans = [self.answers[i].get()[-1] for i in range(len(self.answers))]
            print(ans)
        except IndexError:
            print("Something's missing...")   

        

    
mainmenu = Tk()
menuwindow = MainWindow(mainmenu,'MainMenu')
mainmenu.mainloop()