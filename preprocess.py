import numpy as np
from scipy.misc import imread
import ffmpy
from ffmpy import FFmpeg
import cv2
import os
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches



#change output image names according to each video
def parse_video(video):
	print "Parse_video:", video
	return


def getLines(img): #img is the base_image without hands in it
    base_img = cv2.imread(img) #a static variable above main
    base_img = base_img.astype(np.uint8)
    img_sobel = sobel(base_img)

    cv2.imwrite("video_2-0001_sobel.jpg", img_sobel)
    #apply thresholding to binarize image: http://docs.opencv.org/2.4/doc/tutorials/imgproc/threshold/threshold.html
    thresh, img_binary = cv2.threshold(img_sobel, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite("video_2-0001_binary.jpg", img_binary)
    best_lines = hough(img_binary)
    #right now, best lines is all lines returned by Hough
    return base_img, best_lines


#from https://github.com/abidrahmank/OpenCV2-Python/blob/master/Official_Tutorial_Python_Codes/3_imgproc/sobel.py
def sobel(img):
	scale = 1
	delta = 0
	ddepth = cv2.CV_16S
	#img = cv2.imread(img)
	img = cv2.GaussianBlur(img,(3,3),0) #idk what these numbers mean
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	# Gradient-X
	grad_x = cv2.Sobel(gray,ddepth,1,0, ksize = 3, scale = scale, delta = delta, borderType = cv2.BORDER_DEFAULT)
	#grad_x = cv2.Scharr(gray,ddepth,1,0)
	# Gradient-Y
	grad_y = cv2.Sobel(gray,ddepth,0,1, ksize = 3, scale = scale, delta = delta, borderType = cv2.BORDER_DEFAULT)
	#grad_y = cv2.Scharr(gray,ddepth,0,1)
	abs_grad_x = cv2.convertScaleAbs(grad_x)   # converting back to uint8
	abs_grad_y = cv2.convertScaleAbs(grad_y)
	dst = cv2.addWeighted(abs_grad_x,0.5,abs_grad_y,0.5,0)
	return dst

#http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
def hough(img): #img is a binarized image
    #First parameter, Input image should be a binary image, so apply threshold or use canny edge detection before finding applying hough transform. Second and third parameters are \rho and \theta accuracies respectively. Fourth argument is the threshold, which means minimum vote it should get for it to be considered as a line. Remember, number of votes depend upon number of points on the line. So it represents the minimum length of line that should be detected.

    params = cv2.HoughLines(img, 1,np.pi/180, 100) #params 2 and 3 i got somewhere, 4 we should tune
    #arr is array of (rho, theta) for each line above voting threshold
    over = 0
    under = 0
    for i in xrange(len(params)):
        degrees = 180 * params[i][0][1] / math.pi
        params[i][0][1] = degrees #all angles are positive degree values
        if degrees >= 90:
            over += 1
        else:
            under += 1
    print "over, under 90", over, under
    print params
    #best_lines = sort params (with what qualifications?), take best 2
    return params#best_lines


