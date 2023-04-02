from aruco_video_helper import  aruco_overlay
from imutils.video import VideoStream
from collections import deque
import argparse
import imutils
import time
import cv2

argpar= argparse.ArgumentParser()
argpar.add_argument("-i", "--input", type=str, required=True,
	help="path to input video file for augmented reality")
argpar.add_argument("-u", "--usesaved", type= int, default= -1,
                      help="Use saved reference points?")

args=vars(argpar.parse_args())



print("[INFO] accessing video stream...")
image = cv2.imread(args["input"])

image = imutils.resize(image, width=600)

source= image

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
    frame= vs.read()
    overlay= aruco_overlay(frame, source, useSAVE=args["usesaved"]>0)
    
    if overlay is not None:
        frame= overlay
    
    cv2.imshow("frame", frame)
    key= cv2.waitKey(1) & 0xFF
    
    if key== ord("q"):
        break# this is our function quit
    
cv2.destroyAllWindows()
vs.stop()