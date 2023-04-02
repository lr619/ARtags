import numpy as np
import cv2
#implementing cache to reduce flickering

SAVED_REF_PTS= None

def aruco_overlay(frame, source, useSAVE= True):
    global SAVE_REF_PTS
        
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
    arucoParams = cv2.aruco.DetectorParameters_create()
        
    (imgHeight, imgWidth)= frame.shape[:2]
    (srcHeight, srcWidth)= source.shape[:2]
    
    #detecting arucos
    (corners, ids, rejected)= cv2.aruco.detectMarkers(frame, arucoDict, parameters= arucoParams)
    if (len(corners)!=4):
        return None
    else:
        ids.flatten()
    
    refPts=[]
    for i in (24, 35, 49, 46):#for some reaon its inputing 2 values
        j= np.squeeze(np.where(ids==i))
        print("j: {}, j.size: {}\n".format(j, j.size))
        if j.size==0:
            continue#means not all detected
        corner= np.squeeze(corners[j[0]])
        refPts.append(corner)
         
        
    if len(refPts)!=0:
            
            
        (refPtTL, refPtTR, refPtBR, refPtBL) = refPts
        dstMat = [refPtTL[0], refPtTR[1], refPtBR[2], refPtBL[3]]
        dstMat = np.array(dstMat)
        srcMat = np.array([[0, 0], [srcWidth, 0], [srcWidth, srcHeight], [0, srcHeight]])
        (H, _) = cv2.findHomography(srcMat, dstMat)
        warped = cv2.warpPerspective(source, H, (imgWidth, imgHeight))#needed tos wap this 

        mask = np.zeros((imgHeight, imgWidth), dtype="uint8")
        cv2.fillConvexPoly(mask, dstMat.astype("int32"), (255, 255, 255), cv2.LINE_AA)

        rect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mask = cv2.dilate(mask, rect, iterations=2)

        maskScaled = mask.copy() / 255.0
        maskScaled = np.dstack([maskScaled] * 3)

        warpedMultiplied = cv2.multiply(warped.astype("float"), maskScaled)
        imageMultiplied = cv2.multiply(frame.astype(float), 1.0 - maskScaled)
        output = cv2.add(warpedMultiplied, imageMultiplied)
        output = output.astype("uint8")
        
        return output
    else:
        return None
