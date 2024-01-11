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
IMAGE_PATH = r"C:\Users\pam-s\Desktop\NSHPAM\work\OMR 50k\Python OMR prototype1\test.jpg"
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
pixelsPerMetric = None #resolution
print('Contour found :',len(cnts[0])) #มีซ้ำ
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
		cv2.circle(orig, (int(x), int(y)), 5, (0, 255, 64), -1)#จุดสี่มุม

	(tl, tr, br, bl) = box
	(tltrX, tltrY) = midpoint(tl, tr)
	(blbrX, blbrY) = midpoint(bl, br)

	(tlblX, tlblY) = midpoint(tl, bl)#topleft topright
	(trbrX, trbrY) = midpoint(tr, br)

	cv2.circle(orig, (int(tltrX), int(tltrY)), 0, (0, 255, 64), 0)#จุดแต่ละจุด
	cv2.circle(orig, (int(blbrX), int(blbrY)), 0, (0, 255, 64), 0)
	cv2.circle(orig, (int(tlblX), int(tlblY)), 0, (0, 255, 64), 0)
	cv2.circle(orig, (int(trbrX), int(trbrY)), 0, (0, 255, 64), 0)

	cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
		(0, 0, 255), 1)#axis
	cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
		(0, 0, 255), 1)

	dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))#ความยาวระหว่างจุด
	dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

	if pixelsPerMetric is None:
		pixelsPerMetric = dB / 1.02362205#หน่วยinchเทียบกับmm

	dimA = dA / pixelsPerMetric#คำนวณจากรูปจริง ของสิ่งของในรูป
	dimB = dB / pixelsPerMetric

	cv2.putText(orig, "{:.2f}cm".format(dimA * 2.54),
		(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)
	cv2.putText(orig, "{:.2f}cm".format(dimB * 2.54),
		(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 255, 255), 2)

	# show output
	cv2.imshow("Measuring_Size_Image", orig)
	cv2.waitKey(0)

print('finish')
