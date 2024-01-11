'''#reshape()
import numpy as np
x = np.zeros((4, 1, 2), np.int32) #np.zeros((row,array dimension,column),data type = int 32-bit)
print(x)'''

#imutlis learning
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2

def midpoint(ptA, ptB):
  return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

#IMAGE_PATH = r"C:\Users\pam-s\Desktop\NSHPAM\work\OMR 50k\Python OMR prototype1\measure1.jpeg"
IMAGE_PATH = r'C:\Users\pam-s\Desktop\NSHPAM\work\OMR 50k\Python OMR prototype1\real.jpg'
#IMAGE_PATH = r"C:\Users\pam-s\Desktop\NSHPAM\work\OMR 50k\Python OMR prototype1\test.jpg"
#IMAGE_PATH = r'C:\Users\pam-s\Desktop\NSHPAM\work\OMR 50k\Python OMR prototype1\5.png'

image = cv2.imread(IMAGE_PATH)
image = cv2.resize(image,(700,700))
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1) #has to be binary image(black and white only)
edged = cv2.erode(edged, None, iterations=1)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)#เอามาเฉพาะcnts

(cnts, _) = contours.sort_contours(cnts)
print('Contour found :',len(cnts[0])) #มีซ้ำ
corner = []

def drawGrid(img,questions=5,choices=25):
    secW = int(img.shape[1]/questions)
    secH = int(img.shape[0]/choices)
    for i in range (1,24):
        point1 = (0,secH*(i))
        point2 = (img.shape[1],secH*(i))
        point3 = (secW * i, 0)
        point4 = (secW*i,img.shape[0])
        cv2.line(img, point1, point2, (255, 255, 0),2)#horizontal
        cv2.line(img, point3, point4, (255, 255, 0),2)#vertical

    return img

for c in cnts:
  if cv2.contourArea(c) < 100:
    continue

  orig = image.copy()
  box = cv2.minAreaRect(c)#กำหนดพิกัดมา 4 พิกัดเพื่อให้รูปมันฟิต
  box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
  box = np.array(box, dtype="int")

  box = perspective.order_points(box)
  cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 64), 2)

  for (x, y) in box:
    cv2.circle(orig, (int(x), int(y)), 5, (0, 255, 64), -1)#จุดสี่มุม tl>>>tr>>>br>>>bl

  (tl, tr, br, bl) = box

  pt1 = list(tl)
  pt2 = list(tr)
  pt3 = list(bl)#topleft topright
  pt4 = list(br)
  corner = [pt1,pt2,pt3,pt4]
  print(corner)

  picture1 = np.float32(corner)

  height,width = orig.shape[0],orig.shape[1]//4
  picture2 = np.float32([[0,0] , [width,0] , [0,height] , [width,height]])
  matrix = cv2.getPerspectiveTransform(picture1,picture2)
  output = cv2.warpPerspective(orig,matrix,(width,height))
  print(output.shape[0],output.shape[1]) #[0] height, [1], width

  drawGrid(output)

  cv2.imshow("Original", orig)
  cv2.imshow("Output", drawGrid(output))
  cv2.waitKey(0)

print('finish')