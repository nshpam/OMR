from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from numpy.core.fromnumeric import _all_dispatcher
from pdf2image import convert_from_path
from tkPDFViewer import tkPDFViewer as pdf 
import cv2

MainMenu= Tk()
MainMenu.geometry("750x250")

POPPLER_PATH = r'C:\Program Files\poppler-21.03.0\Library\bin'
all_path = []

def image_path(path_list):
    for imgs_index in range(len(path_list)):
        current_img = cv2.imread(path_list[imgs_index][0])
        #cv2.imshow('img%d'%imgs_index, current_img)
        #cv2.waitKey(0)

def covert_pdf():
    images = convert_from_path(path, poppler_path =POPPLER_PATH)
    file_save = filedialog.askdirectory()
    
    if file_save == '':
        global warn_label
        try:
            path_label.destroy()
        except:
            pass
        else:
            path_label.destroy()
        
        warn_label = Label(Operation_win, text = "Please select your file")
        warn_label.pack(ipadx=8, pady=15)
    else:
        all_path = []
        for i in range(len(images)):
            save_path = file_save+'/test'+ str(i) +'.jpg', 'JPEG'
            images[i].save(file_save+'/test'+ str(i) +'.jpg', 'JPEG')
            all_path.append(save_path)

            bar['value']+=(100//len(images))
            if i == (len(images)-1):
                bar != 100
                bar['value']+=(100-bar['value'])
        image_path(all_path)
        
        print('finish')

def select_file():
    global path
    global path_label
    try:
        warn_label.destroy()
    except:
        pass
    else:
        warn_label.destroy()
    path= filedialog.askopenfilename(title="Select a File", filetype=(('pdf file', '*.pdf'),('all files','*.*')))
    path_label = Label(Operation_win, text=path, font=13).pack(ipadx=8, pady=15)
    return path

def PDF_Preview():

    PDF_win = Toplevel(Operation_win)
    Mypdf = pdf.ShowPdf()
    Preview_PDF = Mypdf.pdf_view(PDF_win, 
                    pdf_location = path,  
                    width = 50, height = 100)

    Preview_PDF.pack()

def Operation():
    HideWindow(MainMenu)
    global Operation_win
    Operation_win = Toplevel(MainMenu)
    Operation_win.geometry("750x500")

    Label(Operation_win, text="Click the Button to Select a File", font=('Aerial 18 bold')).pack(pady=20)
    button1= ttk.Button(Operation_win, text="Select", command= select_file)
    button1.pack(ipadx=5, pady=15)

    button2= ttk.Button(Operation_win, text="Convert", command= covert_pdf)
    button2.pack(ipadx=6, pady=15)

    button3= ttk.Button(Operation_win, text="Preview", command= PDF_Preview)
    button3.pack(ipadx=7, pady=15)

    button4 = ttk.Button(Operation_win, text="Exit", command= MainMenu.destroy)
    button4.pack(ipadx=8, pady=15)

    bar = ttk.Progressbar(Operation_win,orient=HORIZONTAL,length=300,mode="determinate")
    bar.pack(ipadx=9, pady=15)

def CustomAnswerWindow():
    HideWindow(MainMenu)
    print('---Custom Answer Window---')

def ShowWindow(WindowShowed):
    WindowShowed.deiconify()

def HideWindow(WindowHid):
    WindowHid.withdraw()


Label(MainMenu, text="Click the Button to Select Medthod", font=('Aerial 18 bold')).pack(pady=20)

button1 = ttk.Button(MainMenu, text="Custom Answer", command= CustomAnswerWindow)
button1.pack(ipadx=5, pady=15)

button2 = ttk.Button(MainMenu, text="Import PDF", command= Operation)
button2.pack(ipadx=6, pady=15)

button3 = ttk.Button(MainMenu, text="Exit", command= MainMenu.destroy)
button3.pack(ipadx=7, pady=15)

MainMenu.mainloop()