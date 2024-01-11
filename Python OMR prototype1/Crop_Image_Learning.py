#imutlis learning
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2

IMAGE_PATH = r"C:\Users\pam-s\Desktop\NSHPAM\work\OMR 50k\Python OMR prototype1\test.jpg"
#5.png
#unknown (1).png
#real.jpg
#measure1.jpeg

questions = 25
choices = 5

image = cv2.imread(IMAGE_PATH)
#image = cv2.resize(image,(700,700))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (7, 7), 0)

edged = cv2.Canny(blur, 50, 100)
edged = cv2.dilate(edged, None, iterations=1) #has to be binary image(black and white only)
edged = cv2.erode(edged, None, iterations=1)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)#เอามาเฉพาะcnts

cnts = contours.sort_contours(cnts)[0]
#print('Contour found :',len(cnts[0])) #มีซ้ำ
corner = []

'''def drawGrid(img,choices=5,questions=25):
    secW = int(img.shape[1]/choices)
    secH = int(img.shape[0]/questions)
    for i in range (26):
        point1 = (0,secH*(i))
        point2 = (img.shape[1],secH*(i))
        point3 = (secW * i, 0)
        point4 = (secW*i,img.shape[0])
        cv2.line(img, point1, point2, (255, 255, 0),2)#horizontal
        cv2.line(img, point3, point4, (255, 255, 0),2)#vertical

    return img'''

'''def splitBoxes(img):
    rows = np.vsplit(img,questions)
    boxes=[]
    for r in rows:
        cols= np.hsplit(r,choices)
        for box in cols:
            boxes.append(box)
    return boxes'''

'''def midpoint(ptA, ptB):
  return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)'''

count = 0
ROI_number = 0

for c in cnts:
  count+=1
  if cv2.contourArea(c) < 100:
    continue

  orig = image.copy()
  box = cv2.minAreaRect(c)#กำหนดพิกัดมา 4 พิกัดเพื่อให้รูปมันฟิต
  box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
  box = np.array(box, dtype="int")

  box = perspective.order_points(box)
  #print(list(box))
  #print('OBJECT%d:'%count,box[0])   #box[0] = pt1, box[1] = pt2, box[2] = pt3, box[3] = pt4
  #print('X:',box[0][0],'Y:',box[0][1])
  #print(type(box[0][0]))
  #x = float(box[0][0])
  '''cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 64), 2)

  for (x, y) in box:
    cv2.circle(orig, (int(x), int(y)), 5, (0, 255, 64), -1)#จุดสี่มุม tl>>>tr>>>br>>>bl
  (tl, tr, br, bl) = box

  pt1 = list(tl)
  pt2 = list(tr)
  pt3 = list(bl)#topleft topright
  pt4 = list(br)
  corner = [pt1,pt2,pt3,pt4]'''
  #print(pt1)
  #print(corner)
  y1 = int(box[0][1])
  y2 = int(box[2][1])
  x1 = int(box[0][0])
  x2 = int(box[1][0])
  cropped_image = orig[y1:y2, x1:x2]
  thres_crop_img = cv2.threshold(cropped_image,170,255,cv2.THRESH_BINARY_INV)[1]
# cropped__img = img[y1:y2, x1:x2]

  #boxes = splitBoxes(thres_crop_img)
  #cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
  '''blur2 = cv2.GaussianBlur(thres_crop_img, (7, 7), 0)
  edged2 = cv2.Canny(blur2, 50, 100)
  edged2 = cv2.dilate(edged2, None, iterations=1) #has to be binary image(black and white only)
  edged2 = cv2.erode(edged2, None, iterations=1)
  cnts2= cv2.findContours(edged2.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
  cnts2 = cnts2[0] if len(cnts2) == 2 else cnts2[1]'''
  #cnts2 = imutils.grab_contours(cnts2)#เอามาเฉพาะcnts

  '''(cnts2, _) = contours.sort_contours(cnts)
  for c2 in cnts2:

    thresh_original = thres_crop_img.copy()
    box2 = cv2.minAreaRect(c2)#กำหนดพิกัดมา 4 พิกัดเพื่อให้รูปมันฟิต
    box2 = cv2.cv.BoxPoints(box2) if imutils.is_cv2() else cv2.boxPoints(box2)
    box2 = np.array(box2, dtype="int")

    box2 = perspective.order_points(box2)

    cv2.drawContours(thresh_original, [box2.astype("int")], -1, (0, 255, 64), 2)

    for (a, b) in box2:
      cv2.circle(orig, (int(a), int(b)), 5, (0, 255, 64), -1)'''

  '''ROI = thres_crop_img[y:y+h, x:x+w]
  cv2.imshow('image_ROI',ROI)
  cv2.waitKey()'''

  #drawGrid(cropped_image)
#[startY:endY,startX,endX]


  '''picture1 = np.float32(corner)

  height,width = orig.shape[0],orig.shape[1]//4
  picture2 = np.float32([[0,0] , [width,0] , [0,height] , [width,height]])
  matrix = cv2.getPerspectiveTransform(picture1,picture2)
  output = cv2.warpPerspective(orig,matrix,(width,height))
  print(output.shape[0],output.shape[1]) #[0] height, [1], width'''


  cv2.imshow("Original", orig)
  #cv2.imshow('cropped original',thresh_original)
  #cv2.imshow("box0", boxes[0])
  #cv2.imshow("Output",cropped_image)
  #cv2.imwrite('output_grid.png',cropped_image)
  cv2.imshow("Output",thres_crop_img)
  cv2.waitKey(0)
print('finish')

