#!/usr/bin/python

# Copyright (c) 2011, Aaron Fineman
# Based off code by Roman Stanchak and Nirav Patel (http://eclecti.cc)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys, os
from opencv.cv import *
from opencv.highgui import *

haar_file = 'haar/1256617233-1-haarcascade_hand.xml'

def detectObject(image):
  grayscale = cvCreateImage(cvSize(640, 480), 8, 1)
  cvCvtColor(image, grayscale, CV_BGR2GRAY)
  storage = cvCreateMemStorage(0)
  cvClearMemStorage(storage)
  cvEqualizeHist(grayscale, grayscale)
  cascade = cvLoadHaarClassifierCascade(haar_file, cvSize(1,1))
  objects = cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2, 
                              CV_HAAR_DO_CANNY_PRUNING, cvSize(100,100))

  if objects:
    for i in objects:
      cvRectangle(image, cvPoint( int(i.x), int(i.y)),
                  cvPoint(int(i.x+i.width), int(i.y+i.height)),
                  CV_RGB(0,255,0), 3, 8, 0)
  
def displayObject(image):
  cvNamedWindow("objects", 1)
  cvShowImage("objects", image)
  cvWaitKey(0)
  cvDestroyWindow("objects")
  
def main():
  # Uses xawtv. Gstreamer can be used instead, but I found it much slower
  os.system("v4lctl snap jpeg 640x480 /tmp/cam.jpg")
  image = cvLoadImage("/tmp/cam.jpg")
  detectObject(image)
  displayObject(image)
  cvSaveImage("/tmp/cam.jpg", image)

if __name__ == "__main__":
  main()
