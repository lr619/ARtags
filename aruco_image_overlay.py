import numpy as np
import argparse 
import imutils
import sys
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image containing ArUCo tag")
ap.add_argument("-s", "--source", required=True,
	help="path to input source image that will be put on input")
args = vars(ap.parse_args())

print("[INFO] loading input image and source image...")
image = cv2.imread(args["image"])
image = imutils.resize(image, width=600)
(imgH, imgW) = image.shape[:2]

source = cv2.imread(args["source"])
print("[INFO] detecting markers...")
arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)# need to constantly change
arucoParams = cv2.aruco.DetectorParameters_create()
(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,
	parameters=arucoParams)

if len(corners) != 4:
	print("[INFO] could not find 4 corners...exiting")
	sys.exit(0)
 
print("[INFO] contstructing AR visual ")

ids= ids.flatten()
refPts= []

for i in (24,35,49,46):#tells us to loop through current IDS
    j = np.squeeze(np.where(ids == i))
    print("j:{}, j.size{}".format(j, j.size))
    corner = np.squeeze(corners[j])
    refPts.append(corner)
    
#save reference points to create the deistination matrix
(refPtTL, refPtTR, refPtBR, refPtBL) = refPts
dstMat = [refPtTL[0], refPtTR[1], refPtBR[2], refPtBL[3]]
dstMat = np.array(dstMat)

(srcH, srcW)= source.shape[:2] #orders it
srcMat = np.array([[0, 0], [srcW, 0], [srcW, srcH], [0, srcH]])
 
 
(H, _) = cv2.findHomography(srcMat, dstMat)
warped = cv2.warpPerspective(source, H, (imgW, imgH))

mask = np.zeros((imgH, imgW), dtype="uint8")
cv2.fillConvexPoly(mask, dstMat.astype("int32"), (255, 255, 255),
	cv2.LINE_AA)

rect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
mask = cv2.dilate(mask, rect, iterations=2)

maskScaled = mask.copy() / 255.0
maskScaled = np.dstack([maskScaled] * 3)

warpedMultiplied = cv2.multiply(warped.astype("float"), maskScaled)
imageMultiplied = cv2.multiply(image.astype(float), 1.0 - maskScaled)
output = cv2.add(warpedMultiplied, imageMultiplied)
output = output.astype("uint8")

cv2.imshow("Input", image)
cv2.imshow("Source", source)
cv2.imshow("OpenCV AR Output", output)
cv2.waitKey(0)