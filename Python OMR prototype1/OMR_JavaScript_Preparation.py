#Library
import cv2
import numpy as np

#variables
IMAGE_PATH = r'C:\Users\pam-s\Desktop\NSHPAM\work\OMR 50k\Python OMR prototype1\paper_6.png'
questions = 25
choices = 5
ans = [1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,1]

#Spilt Image Function
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
    return boxes

#Show answers function
def showAnswers(img,myIndex,grading,ans,questions=25,choices=5):
    img = cv2.resize(img,(int(img.shape[1]),int(img.shape[0])))
    overlay = img.copy()
    secW = int(img.shape[1]/choices)
    secH = int(img.shape[0]/questions)

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

def get_opencv_major_version(lib=None):
    if lib is None:
        import cv2

    return int(cv2.__version__.split(".")[0])

def is_cv2(or_better=False):
    major = get_opencv_major_version()

    if or_better:
        return major >= 2

    return major == 2

def grab_contours(cnts):
    if len(cnts) == 2:
        cnts = cnts[0]
    elif len(cnts) == 3:
        cnts = cnts[1]
    else:
        raise Exception(("Contours tuple must have length 2 or 3, "
            "otherwise OpenCV changed their cv2.findContours return "
            "signature yet again. Refer to OpenCV's documentation "
            "in that case"))

    return cnts

def reorder(myPoints):

    myPoints = myPoints.reshape((4, 2))
    print(myPoints)
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    print(add)
    print(np.argmax(add))
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] =myPoints[np.argmax(add)]   
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]  
    myPointsNew[2] = myPoints[np.argmax(diff)] 

    return myPointsNew

def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0

    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))

    return cnts, boundingBoxes

#contours
image = cv2.imread(IMAGE_PATH)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)

edged = cv2.Canny(blur, 50, 100)
edged = cv2.dilate(edged, None, iterations=1) #has to be binary image(black and white only)
edged = cv2.erode(edged, None, iterations=1)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = grab_contours(cnts)#เอามาเฉพาะcnts
cnts = sort_contours(cnts)[0]#ถ้าไม่ใส่จะเรียงจากหลังมาหน้า

save_index = 0

color = [(255, 0, 0),(0, 255, 0),(0, 0, 255),(0, 255, 255)]
arealist = []
#filtering frame

for c in cnts:
    if cv2.contourArea(c) < 1500:
        continue
    area = cv2.contourArea(c)
    digit = area

    digitcount = 0
    while(digit>0):
        digitcount+=1
        digit=digit//10
        if len(str(int(digit))) == 2:
            break

    digit = digit*(10**digitcount)
    arealist.append(area)
arealist.sort(reverse=True)
#print(arealist)

for c in cnts:
    
    if cv2.contourArea(c) < min(arealist):
        continue
    if cv2.contourArea(c) == min(arealist):
        print('detected address frame!')
    else:
        
 #find corner points
        orig = image.copy()
        box = cv2.minAreaRect(c)#กำหนดพิกัดมา 4 พิกัดเพื่อให้รูปมันฟิต
        box = cv2.cv.BoxPoints(box) if is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        box = reorder(box)

        (tl, tr, br, bl) = box
        pt1 = list(box[0][0])
        pt2 = list(box[1][0])
        pt3 = list(box[2][0])#topleft topright
        pt4 = list(box[3][0])
        corner = [pt1,pt2,pt3,pt4]

        #perspective
        picture1 = np.float32(corner)
        height,width = orig.shape[0],orig.shape[1]
        picture2 = np.float32([[0,0] , [width,0] , [0,height] , [width,height]])
        matrix = cv2.getPerspectiveTransform(picture1,picture2)
        output = cv2.warpPerspective(orig,matrix,(width,height))
        gray_output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        thres_img = cv2.threshold(gray_output,170,255,cv2.THRESH_BINARY_INV)[1]
        boxes = SplitBox(thres_img)

        #answer collecting
        countR = 0
        countC = 0
        myPixelVal = np.zeros((questions,choices))
        for img in boxes:
            totalPixels = cv2.countNonZero(img)
            myPixelVal[countR][countC] = totalPixels
            countC+=1
            if (countC==choices):countC=0;countR+=1

        myIndex = []
        for pixel_list in myPixelVal:
            currentlist = list(pixel_list)
            margin = 0.75*np.max(myPixelVal)
            anscount = sum([1 if i>margin else 0 for i in currentlist])
            if anscount != 1:
                myIndex.append('f')
            else:
                myIndex.append(currentlist.index(max(currentlist)))

        #print(myIndex)
        
        #score collecting
        grading=[]
        for grade in range(questions):
            if ans[grade] == myIndex[grade]:
                grading.append(1)
            elif ans[grade] == 'f':
                grading.append(0)
            else:
                grading.append(0)
        score = sum(grading)
        print("SCORE",score)
        print("GRADING",grading)

        #save
        save_index+=1
        cv2.imwrite('Result_%d.png'%save_index,showAnswers(output,myIndex,grading,ans))
    
print('finish')
