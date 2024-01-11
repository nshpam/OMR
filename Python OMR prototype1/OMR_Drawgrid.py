import cv2
import numpy as np
from imutils import perspective
from imutils import contours
import imutils

IMAGE_PATH = r'C:\Users\pam-s\Desktop\NSHPAM\work\OMR 50k\25Marks_Ans.png'
count = 0
questions = 25
choices = 5
ans = [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1]
#paper_3.png
#paper.png
#test.jpg
#cropped_image.png
#design1.png

image = cv2.imread(IMAGE_PATH)
#image = cv2.resize(image,(700,700))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)

edged = cv2.Canny(blur, 50, 100)
edged = cv2.dilate(edged, None, iterations=1) #has to be binary image(black and white only)
edged = cv2.erode(edged, None, iterations=1)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)#เอามาเฉพาะcnts
cnts = contours.sort_contours(cnts)[0]#ถ้าไม่ใส่จะเรียงจากหลังมาหน้า

#Spilt Image
def SplitBox(img):
    h = img.shape[0]
    w = img.shape[1]
    if h%questions != 0:
        num = round(h/questions)
        h = num*questions
    if w%choices != 0:
        num = round(w/choices)
        w = num*choices
    img = cv2.resize(img,(w,h))
    rows = np.vsplit(img,questions)
    boxes = []
    for r in rows:
        cols = np.hsplit(r,choices)
        for choice_box in cols:
            boxes.append(choice_box)
    #print(img.shape)
    return boxes

#drawgrid
def drawGrid(img,choices=5,questions=25):
    img = cv2.resize(img,(int(img.shape[1]),int(img.shape[0])))
    secW = int(img.shape[1]/choices)
    secH = int(img.shape[0]/questions)
    for i in range (26):
        point1 = (0,secH*(i))
        point2 = (img.shape[1],secH*(i))
        point3 = (secW * i, 0)
        point4 = (secW*i,img.shape[0])
        cv2.line(img, point1, point2, (255, 255, 0),2)#horizontal
        cv2.line(img, point3, point4, (255, 255, 0),2)#vertical

    return img

def showAnswers(img,myIndex,grading,ans,questions,choices):
    img = cv2.resize(img,(int(img.shape[1]),int(img.shape[0])))
    overlay = img.copy()
    secW = int(img.shape[1]/choices)
    secH = int(img.shape[0]/questions)
    #print(secW)
    #print(secH)

    for rows in range(questions):
        myAns= myIndex[rows]
    
        if myAns == 'f':
            pt1 = (0,secH*rows)#tl  
            pt4 = (secW*choices,secH*(rows+1))#br
            img_rec =cv2.rectangle(overlay, pt1, pt4, (0, 255, 255),-1)

            myAns= ans[rows]
            pt1 = (secW*myAns,secH*rows)#tl  
            pt4 = (secW*(myAns+1),secH*(rows+1))#br
            img_rec = cv2.rectangle(img_rec, pt1, pt4, (255, 0, 0),-1)
        elif grading[rows] == 1:
            pt1 = (secW*myAns,secH*rows)#tl  
            pt4 = (secW*(myAns+1),secH*(rows+1))#br
            img_rec = cv2.rectangle(overlay, pt1, pt4, (0, 255, 0),-1)
        else:
            pt1 = (secW*myAns,secH*rows)#tl  
            pt4 = (secW*(myAns+1),secH*(rows+1))#br
            img_rec = cv2.rectangle(overlay, pt1, pt4, (0, 0, 255),-1)

            myAns= ans[rows]
            pt1 = (secW*myAns,secH*rows)#tl  
            pt4 = (secW*(myAns+1),secH*(rows+1))#br
            img_rec = cv2.rectangle(img_rec, pt1, pt4, (255, 0, 0),-1)

        img_output = cv2.addWeighted(img_rec, 1, img, 0.5, 0)

    return img_output




color = [(255, 0, 0),(0, 255, 0),(0, 0, 255),(0, 255, 255)]
#[BLUE(tl),GREEN(tr),RED(br),YELLOW(bl)]
countimg=0
draw_img = image.copy()
for c in cnts:
    countimg+=1
    #area filter
    if cv2.contourArea(c) < 1500:
        continue
    #find corner points
    orig = image.copy()
    box = cv2.minAreaRect(c)#กำหนดพิกัดมา 4 พิกัดเพื่อให้รูปมันฟิต
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")

    box = perspective.order_points(box)

    (tl, tr, br, bl) = box
    pt1 = list(tl)
    pt2 = list(tr)
    pt3 = list(bl)#topleft topright
    pt4 = list(br)
    corner = [pt1,pt2,pt3,pt4]

    #perspective
    picture1 = np.float32(corner)
    height,width = orig.shape[0],orig.shape[1]
    picture2 = np.float32([[0,0] , [width,0] , [0,height] , [width,height]])
    matrix = cv2.getPerspectiveTransform(picture1,picture2)
    output = cv2.warpPerspective(orig,matrix,(width,height))
    gray_output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    thres_img = cv2.threshold(gray_output,170,255,cv2.THRESH_BINARY_INV)[1]

    cv2.imwrite('anstest_%d.png'%countimg,drawGrid(output,5,25))
    #boxes = SplitBox(thres_img)
    
    '''#show answer
    countR = 0
    countC = 0
    myPixelVal = np.zeros((questions,choices))
    for img in boxes:
        totalPixels = cv2.countNonZero(img)
        myPixelVal[countR][countC] = totalPixels
        countC+=1
        if (countC==choices):countC=0;countR+=1
    
    #print(myPixelVal)

    myIndex = []
    for pixel_list in myPixelVal:
        currentlist = list(pixel_list)
        margin = 0.75*np.max(myPixelVal)
        anscount = sum([1 if i>margin else 0 for i in currentlist])
        if anscount != 1:
            myIndex.append('f')
        else:
            myIndex.append(currentlist.index(max(currentlist)))
                
    #print(myIndexVal) 
    print(myIndex)
    #print(len(myIndex))
        
    grading=[]
    for grade in range(questions):
        if ans[grade] == myIndex[grade]:
            grading.append(1)
        elif ans[grade] == 'f':
            grading.append(0)
        else:
            grading.append(0)
    score = sum(grading)
    #score = (sum(grading)/questions)*100
    print("SCORE",score)
    print("GRADING",grading)
    cv2.imwrite('anstest_%d.png'%countimg,showAnswers(output,myIndex,grading,ans))'''
    
print('finish')
