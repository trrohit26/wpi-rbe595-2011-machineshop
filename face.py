#!/usr/bin/python

# Face Detection using OpenCV. Based on sample code by Roman Stanchak
# Nirav Patel http://eclecti.cc 5/20/2008

import sys, os
from opencv.cv import *
from opencv.highgui import *

haar_file = 'haar/1256617233-1-haarcascade_hand.xml'
image_file = 'pictures/hand.jpg'

def detectObject(image):
  grayscale = cvCreateImage(cvSize(640, 480), 8, 1)
  cvCvtColor(image, grayscale, CV_BGR2GRAY)
  storage = cvCreateMemStorage(0)
  cvClearMemStorage(storage)
  cvEqualizeHist(grayscale, grayscale)
  cascade = cvLoadHaarClassifierCascade(haar_file, cvSize(1,1))
  faces = cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2, 
                              CV_HAAR_DO_CANNY_PRUNING, cvSize(100,100))
  print faces
  if faces:
    for i in faces:
      cvRectangle(image, cvPoint( int(i.x), int(i.y)),
                  cvPoint(int(i.x+i.width), int(i.y+i.height)),
                  CV_RGB(0,255,0), 3, 8, 0)
  
def displayObject(image):
  cvNamedWindow("face", 1)
  cvShowImage("face", image)
  cvWaitKey(0)
  cvDestroyWindow("face")
  
def main():
  # Uses xawtv. Gstreamer can be used instead, but I found it much slower
  os.system("v4lctl snap jpeg 640x480 /tmp/face.jpg")
  image = cvLoadImage("/tmp/face.jpg")
  detectObject(image)
  displayObject(image)
  cvSaveImage("/tmp/face.jpg", image)

if __name__ == "__main__":
  main()
