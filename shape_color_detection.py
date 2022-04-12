import cv2
import numpy as np
from matplotlib import pyplot as plt
d={}
l=[]
# reading image
img = cv2.imread(r'C:\Users\bhara\Desktop\workspace\shapes1.jpeg')
# converting image into grayscale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

red_lower = np.array([0, 100, 20], np.uint8)
red_upper = np.array([180, 255, 255], np.uint8)

green_lower = np.array([25, 52, 72], np.uint8)
green_upper = np.array([102, 255, 255], np.uint8)

blue_lower = np.array([94, 80, 2], np.uint8)
blue_upper = np.array([120, 255, 255], np.uint8)

kernal = np.ones((5, 5), "uint8")


# setting threshold of gray image
_, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
  
# using a findContours() function
contours, _ = cv2.findContours(
    threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  
i = 0
  
# list for storing names of shapes
for contour in contours:
  
    # here we are ignoring first counter because 
    # findcontour function detects whole image as shape
    if i == 0:
        i = 1
        continue
  
    # cv2.approxPloyDP() function to approximate the shape
    approx = cv2.approxPolyDP(
        contour, 0.01 * cv2.arcLength(contour, True), True)
      
    # using drawContours() function
    cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)
  
    # finding center point of shape
    M = cv2.moments(contour)
    if M['m00'] != 0.0:
        x = int(M['m10']/M['m00'])
        y = int(M['m01']/M['m00'])

    crop = img[y-10:y+10, x-10:x+10]

    hsv_img = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

    red_mask = cv2.inRange(hsv_img, red_lower, red_upper)
    green_mask = cv2.inRange(hsv_img, green_lower, green_upper)
    blue_mask = cv2.inRange(hsv_img, blue_lower, blue_upper)

    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(crop, crop,
                                    mask = red_mask)
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(crop, crop,
                                    mask = green_mask)
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(crop, crop,
                                    mask = blue_mask)

    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if 'red' not in d:
            d['red']=[]
        color='red'

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if 'green' not in d:
            d['green']=[]
        color='green'

    # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if 'blue' not in d:
            d['blue']=[]
        color='blue'
  
    # putting shape name at center of each shape
    if len(approx) == 3:
        l.append([color,'tri',(x,y)])
  
    elif len(approx) == 4:
        l.append([color,'quad',(x,y)])
  
    elif len(approx) == 5:
        l.append([color,'pent',(x,y)])
  
    elif len(approx) == 6:
        l.append([color,'hex',(x,y)])
  
    else:
        l.append([color,'cir',(x,y)])
  
print(l)