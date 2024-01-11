import imutils
from imutils import contours
from imutils.perspective import four_point_transform
import numpy as np
import cv2
from random import randint

# Randomly generating the answers
answer = {}

for i in range(26):
    answer[i] = randint(0,3)
    answer[i+25] = randint(0,3)
    answer[i+50] = randint(0,3)
    answer[i+75] = randint(0,3) 

ANSWER = [(k, v) for k, v in answer.items()]


# Loading the image
image = cv2.imread(r'C:\Users\pam-s\Desktop\NSHPAM\work\OMR 50k\Python OMR prototype1\test.jpg')

# OPTIONAL: cropping random objects appearing in the original image
# though recommended to crop the image into only the working space
# to prevent detecting unnecessary objects
image = image[30:1420, 0:1426]
# Resizing the image
image = imutils.resize(image, height = 900)

# Transforming image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Thresholding the image
# Mess around with the thresh and max value to be able to detect
# the contours accordingly
thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)[1]

# Taking all of the contours in the image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
qust_cnts = []

# looping through each contours
for c in cnts:
    # getting the dimension and position of each contour
    (x, y, w, h) = cv2.boundingRect(c)
    ar = w / float(h)

    # validating if they are the contours for the questions
    if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
        qust_cnts.append(c)
        # print(f'X: {x} | Y: {y}')

"""
Two simple functions to extract the coordinates of each contour
"""
def get_x(contour):
    (x, y, w, h) = cv2.boundingRect(contour)
    return x
def get_y(contour):
    (x, y, w, h) = cv2.boundingRect(contour)
    return y

# getting the y-coordinates of all contours to create bins to sort
# them line by line
y = [get_y(c) for c in qust_cnts]
# print(len(y)) it should be 400 here since there are 100 questions 
# and 4 answers to each question

# creating 24 bins to fit 25 ranges of y-values to sort them accordingly
# a little problem with sorting by either y or x or even both
# is that if the pixel value flucuate by even 1 pixel, the order
# of the contours will be changed completely
freq, bins = np.histogram(y, bins=24, density=True)


# adding contours according to the bin of their y-coordinates
y = [[c for c in qust_cnts if i-18<=get_y(c)<=i+17] for i in bins]

# each line should contain only 16 values representing 4 answers 
# to each question and 4 questions in each line
for i, lc in enumerate(y):
    if (len(lc)) != 16:
        # if any line has more than 16 contours, print out
        # the corresponding index and the length as well as the bin
        print(f'Index: {i} Length: {len(lc)} Bin: {bins[i]}')
    else: 
        pass

# once we made sure that the contours have been sorted by their
# y-coordinates or simply by each line, we sort them once again by 
# their x-coordinates in each line
sorted_cnts = [sorted(lc, key=get_x) for lc in y]


# unpacking the list 
question_cnts = []
for lc in sorted_cnts:
    for c in lc:
        question_cnts.append(c)

# another way to do this is to use tools from the package imutils 
# it requires higher pixel-value accuracy and was not accurate in the image
# I chose so I made my own sorting method
# qust_cnts = contours.sort_contours(qust_cnts, method='top-to-bottom')[0]
correct = 0

for x, i in enumerate(np.arange(0, len(question_cnts), 4)):
    # since we have 100 questions with 4 answers to each question
    # we are making an array from 0 to 400 with step of 4

    # sorting the contours from left to right (default arg)
    # to recognize the correct 
    # cnts = contours.sort_contours(qust_cnts[i:i+4], method='left-to-right')[0]
    cnts = question_cnts[i:i+4]
    bubbled = None

    for z, c in enumerate(cnts):
        # making a mask of zeros for the threshold image
        mask = np.zeros(thresh.shape, dtype='uint8')

        # drawing the contours for the first 4 contours in the sorted list
        cv2.drawContours(mask, [c], -1, 255, 2)

        # applying the mask of zeros to the threshold image
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)

        # count the non zero pixel
        total = cv2.countNonZero(mask)

        # since the blacked out bubble will have the max amount of non-zero
        # in order words, the least amount of zeros 
        # its index will be the choice that the user took

        if bubbled is None or total > bubbled[0]:
            # adding the index position (z variable) to the bubble to compare
            bubbled = (total, z)

    color = (0, 0, 255) # red
    k = ANSWER[x][1] 

    if k == bubbled[1]:
        color = (0, 255, 0) # green
        correct += 1

    print(f"Question: {ANSWER[x][0]} | Answer: {k} | Choice {bubbled[1]}")
    # draw the contour accordingly
    cv2.drawContours(image, [cnts[k]], -1, color, 2)
    #cv2.imshow('check', image)
    cv2.waitKey(0)
cv2.destroyAllWindows()

score = (correct / 100.0) * 100
cv2.putText(image, f"{round(score, 2)}", (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
cv2.imshow("Graded", image)
cv2.waitKey(0)
cv2.imwrite('graded.png', image)
cv2.destroyAllWindows()

