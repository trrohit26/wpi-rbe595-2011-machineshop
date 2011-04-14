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

import sys, os, signal
import math
import opencv
from opencv import cv
from opencv import highgui
import playerc

haar_file = '../haar/1256617233-1-haarcascade_hand.xml'
size = cv.cvSize(640, 480)
camera = highgui.cvCreateCameraCapture(0)

max_speed = 0.5 # m/s
speed_left = 0
speed_right = 0
speed = (0, 0)

box_forward_left = (cv.cvPoint(50,60), cv.cvPoint(140,240))
box_forward_right = (cv.cvPoint(500,60), cv.cvPoint(590,240))
box_backwards_left = (cv.cvPoint(50,240), cv.cvPoint(140,420))
box_backwards_right = (cv.cvPoint(500,240), cv.cvPoint(590,420))

def detectObject(image):
  grayscale = cv.cvCreateImage(size, 8, 1)
  cv.cvFlip(image, None, 1)
  cv.cvCvtColor(image, grayscale, cv.CV_BGR2GRAY)
  storage = cv.cvCreateMemStorage(0)
  cv.cvClearMemStorage(storage)
  cv.cvEqualizeHist(grayscale, grayscale)
  cascade = cv.cvLoadHaarClassifierCascade(haar_file, cv.cvSize(1,1))
  objects = cv.cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2, 
                                   cv.CV_HAAR_DO_CANNY_PRUNING,
                                   cv.cvSize(100,100))

  # Draw dots where hands are
  if objects:
    for i in objects:
      #cv.cvRectangle(image, cv.cvPoint( int(i.x), int(i.y)),
      #               cv.cvPoint(int(i.x+i.width), int(i.y+i.height)),
      #               cv.CV_RGB(0,255,0), 3, 8, 0)
      center = cv.cvPoint(int(i.x+i.width/2), int(i.y+i.height/2))
      cv.cvCircle(image, center, 10, cv.CV_RGB(0,0,0), 5,8, 0)
      # Left side check
      if center.x > box_forward_left[0].x and center.x < box_backwards_left[1].x and center.y > box_forward_left[0].y and center.y < box_backwards_left[1].y:
        set_speed('left', center)
      # Right side check
      if center.x > box_forward_right[0].x and center.x < box_backwards_right[1].x and center.y > box_forward_right[0].y and center.y < box_backwards_right[1].y:
        set_speed('right', center)

def handler(signum, frame):
  sys.exit(0)

def get_image():
  img = highgui.cvQueryFrame(camera)
  #img = opencv.cvGetMat(img)
  return opencv.adaptors.Ipl2PIL(img)

def draw_gui(image):
  # Reverse areas
  cv.cvRectangle(image,box_backwards_left[0],box_backwards_left[1],
                 cv.CV_RGB(255,0,0),3,8,0)
  cv.cvRectangle(image,box_backwards_right[0],box_backwards_right[1],
                 cv.CV_RGB(255,0,0),3,8,0)
  # Forward areas
  cv.cvRectangle(image,box_forward_left[0],box_forward_left[1],                             cv.CV_RGB(0,255,0),3,8,0)
  cv.cvRectangle(image,box_forward_right[0],box_forward_right[1],
                 cv.CV_RGB(0,255,0),3,8,0)

def set_speed(side, center):
  global speed, speed_left, speed_right

  height = box_forward_left[1].y - box_forward_left[0].y
  magnitude = float(height - center.y)
  magnitude = float(max_speed * magnitude / height)

  if side == 'left': speed_left = magnitude
  if side == 'right': speed_right = magnitude

  speed = (float((speed_left + speed_right)/2), float(math.atan((speed_right - speed_left)/0.3)))
  print speed

def main():
  # Initialization
  highgui.cvNamedWindow("Guardian", 1)

  signal.signal(signal.SIGINT, handler)
  # Stage
  #robot = playerc.playerc_client(None, "localhost", 6665)
  # Corobot
  robot = playerc.playerc_client(None, "corobot-w.wifi.wpi.edu", 6665)

  robot.connect()

  p2dproxy = playerc.playerc_position2d(robot, 0)
  p2dproxy.subscribe(playerc.PLAYERC_OPEN_MODE)
  p2dproxy.get_geom()

  robot.read()

  while True:
    image = highgui.cvQueryFrame(camera)
    detectObject(image)

    p2dproxy.set_cmd_vel(speed[0], 0, speed[1], 0)

    draw_gui(image)
    highgui.cvShowImage("Guardian", image)

    if highgui.cvWaitKey(20) != -1:
      break

  highgui.cvDestroyWindow("Guardian")
  p2dproxy.set_cmd_vel(0, 0, 0, 0)

if __name__ == "__main__":
  main()
