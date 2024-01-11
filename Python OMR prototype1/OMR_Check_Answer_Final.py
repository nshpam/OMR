#Library
import cv2
import numpy as np
from imutils import perspective
from imutils import contours
import imutils
import os

#Variables
FOLDER = r'C:\Users\pam-s\Desktop\NSHPAM\work\OMR 50k\Image_Folder'
ans = [1, 2, 2, 2, 1, 2, 1, 3, 3, 2, 3, 3, 4, 2, 3, 4, 4, 3, 1, 1, 1, 4, 3, 2, 4]

#Spilt image function
def SplitBox(img,choices,questions,vertical):
    h = img.shape[0]
    w = img.shape[1]
    if h%questions != 0:
        num = round(h/questions)
        h = num*questions
    if w%choices != 0:
        num = round(w/choices)
        w = num*choices
    img = cv2.resize(img,(w,h))
    boxes = []

    #Vertical check
    if vertical == True:
        cols = np.hsplit(img,choices)
        for col in cols:
            rows = np.vsplit(col,questions)
            for choice_box in rows:
                boxes.append(choice_box)

    #Horizontal check
    else:
        rows = np.vsplit(img,questions)
        for r in rows:
            cols = np.hsplit(r,choices)
            for choice_box in cols:
                boxes.append(choice_box)
    return boxes

#Show answers function
def showAnswers(img,myIndex,grading,ans,questions,choices):
    img = cv2.resize(img,(int(img.shape[1]),int(img.shape[0])))
    overlay = img.copy()
    secW = int(img.shape[1]/choices)
    secH = int(img.shape[0]/questions)

    for rows in range(questions):
        myAns= myIndex[rows]
        #Wrong answers
        if myAns == 'f':
            pt1 = (0,secH*rows)                     #topleft  
            pt4 = (secW*choices,secH*(rows+1))      #bottomright
            img_rec =cv2.rectangle(overlay, pt1, pt4, (0, 255, 255),-1)

            myAns= ans[rows]
            pt1 = (secW*myAns,secH*rows)            #topleft  
            pt4 = (secW*(myAns+1),secH*(rows+1))    #bottomright
            img_rec = cv2.rectangle(img_rec, pt1, pt4, (255, 0, 0),-1)

        #Correct answers
        elif grading[rows] == 1:
            pt1 = (secW*myAns,secH*rows)            #topleft  
            pt4 = (secW*(myAns+1),secH*(rows+1))    #bottomright
            img_rec = cv2.rectangle(overlay, pt1, pt4, (0, 255, 0),-1)

        #Answers
        else:
            pt1 = (secW*myAns,secH*rows)            #topleft  
            pt4 = (secW*(myAns+1),secH*(rows+1))    #bottomright
            img_rec = cv2.rectangle(overlay, pt1, pt4, (0, 0, 255),-1)

            myAns= ans[rows]
            pt1 = (secW*myAns,secH*rows)            #topleft  
            pt4 = (secW*(myAns+1),secH*(rows+1))    #bottomright
            img_rec = cv2.rectangle(img_rec, pt1, pt4, (255, 0, 0),-1)

        #img_output = cv2.addWeighted(img_rec, 1, img, 1, 0)

    return img_rec

#Image in folder
for imgs in os.listdir(FOLDER):
    image = cv2.imread(os.path.join(FOLDER,imgs))
   
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    edged = cv2.Canny(blur, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1) #has to be binary image(black and white only)
    edged = cv2.erode(edged, None, iterations=1)

    #Contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)#เอามาเฉพาะcnts
    cnts = contours.sort_contours(cnts)[0]#ถ้าไม่ใส่จะเรียงจากหลังมาหน้า

    save_index = 0
    total = 0
    draw_img = image.copy()
    area = []

    #Filters
    for c in cnts:
        if cv2.contourArea(c) < 1500:
                continue
        area.append(cv2.contourArea(c))
    area.sort(reverse=True)
    address = {'SID':'','SUBID':''}

    for c in cnts:
        
        #Filters
        if cv2.contourArea(c) not in area:
            continue
        #Find corner points
        orig = image.copy()
        
        box = cv2.minAreaRect(c) #Fit object with rectangle
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        box = perspective.order_points(box)

        (tl, tr, br, bl) = box
        pt1 = list(tl)
        pt2 = list(tr)
        pt3 = list(bl)
        pt4 = list(br)
        corner = [pt1,pt2,pt3,pt4]

        #Perspective
        picture1 = np.float32(corner)
        height,width = orig.shape[0],orig.shape[1]
        picture2 = np.float32([[0,0] , [width,0] , [0,height] , [width,height]])
        matrix = cv2.getPerspectiveTransform(picture1,picture2)
        output = cv2.warpPerspective(orig,matrix,(width,height))

        gray_output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

        thres_img = cv2.threshold(gray_output,170,255,cv2.THRESH_BINARY_INV)[1]

        #Bubble Column
        if cv2.contourArea(c) in area[:-2]:
            questions = 25
            choices = 5

            #Split images
            boxes = SplitBox(thres_img,choices,questions,False)

            countR = 0
            countC = 0
            myPixelVal = np.zeros((questions,choices))
            
            #Count white pixel
            for img in boxes:
                totalPixels = cv2.countNonZero(img)
                myPixelVal[countR][countC] = totalPixels
                countC+=1
                if (countC==choices):countC=0;countR+=1
            
            #Find max white pixel
            myIndex = []
            for pixel_list in myPixelVal:
                currentlist = list(pixel_list)
                margin = 0.75*np.max(myPixelVal)
                anscount = sum([1 if i>margin else 0 for i in currentlist])
                if anscount != 1:
                        myIndex.append('f')
                else:
                    myIndex.append(currentlist.index(max(currentlist)))
            
            #Answer Checking
            grading=[]
            for grade in range(questions):
                if ans[grade] == myIndex[grade]:
                    grading.append(1)
                elif ans[grade] == 'f':
                    grading.append(0)
                else:
                    grading.append(0)
            score = sum(grading)
            #print("SCORE",score)
            #print("GRADING",grading)
            total += score

            #Paste answer coloring
            cropped_image = draw_img[int(tl[1]):int(br[1]),int(tl[0]):int(br[0])]
            final_image = showAnswers(output,myIndex,grading,ans,questions,choices)
            height,width = cropped_image.shape[0],cropped_image.shape[1]
            final_image = cv2.resize(final_image,(width,height))
            draw_img[int(tl[1]):int(br[1]),int(tl[0]):int(br[0])] = final_image
            #cv2.imwrite('Result_%d.png'%save_index,draw_img)
            #print(myPixelVal)

        #Address Column
        elif cv2.contourArea(c) not in area[:-2]:
            #SID
            if cv2.contourArea(c) == area[-2]:
                questions = 10
                choices = 5
            #Subject ID
            elif cv2.contourArea(c) == area[-1]:
                questions = 10
                choices = 4
            
            #Split images
            boxes = SplitBox(thres_img,choices,questions,True)

            #Count white pixel
            countR = 0
            countC = 0
            myPixelVal = np.zeros((choices,questions))
            for img in boxes:
                totalPixels = cv2.countNonZero(img)
                myPixelVal[countC][countR] = totalPixels
                countR+=1
                if (countR==questions):countR=0;countC+=1
            
            #Answer Checking
            myIndex = []
            for pixel_list in myPixelVal:
                currentlist = list(pixel_list)
                margin = 0.7*np.max(myPixelVal)
                anscount = sum([1 if i>margin else 0 for i in currentlist])
                if anscount != 1:
                        myIndex.append('f')
                else:
                    myIndex.append(currentlist.index(max(currentlist)))
            #print(myIndex)
            
            #Append Address
            for num in range(len(myIndex)):
                if len(myIndex) == 4:
                    address['SUBID']+=str(myIndex[num])
                elif len(myIndex) == 5:
                    address['SID']+=str(myIndex[num])

    #Saving
    save_index+=1
    print(address)
    imgs_name = imgs[:imgs.find('.')] 
    print(imgs_name,'=',total)
    cv2.imwrite(os.path.join(FOLDER,'%s_%d.png'%(imgs_name,save_index)),draw_img)

print('finish')
