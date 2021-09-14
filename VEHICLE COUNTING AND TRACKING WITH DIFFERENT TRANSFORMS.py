import cv2
import numpy as np
import time

min_ctr_width=40  
min_ctr_height=40  
offset=10       
line_y=550 
matches =[]
cars=0
def get_centroid(x, y, w, h):
    xc = int(w / 2)
    yc = int(h / 2)

    ctdx = x + xc
    ctdy = y + yc
    return ctdx,ctdy
    #return (cx, cy)
        
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0)


cap.set(3,1080)
cap.set(4,1080)

if cap.isOpened():
    ret,frame1 = cap.read()
else:
    ret = False

ret,frame1 = cap.read()
ret,frame2 = cap.read()

xcor=[]
ycor=[]
    
while ret:
    time.sleep(.00001)
    extra= frame1.copy()
    extra1=frame1.copy()
    bkgdsub = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(bkgdsub,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    
    
    ret , thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh,np.ones((3,3)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel) 
    contours,heirch = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for(i,c) in enumerate(contours):
        (x,y,w,h) = cv2.boundingRect(c)
        xcor.append(x)
        ycor.append(y)
        contour_valid = False
        if (w >= min_ctr_width) and (h >= min_ctr_height):
            contour_valid = True

        if not contour_valid:
            continue
        
        cv2.rectangle(frame1,(x-10,y-10),(x+w+10,y+h+10),(0,255,255),2)
        
        cv2.line(frame1, (0, line_y), (1200, line_y), (255,255,0), 2)
        centroid = get_centroid(x, y, w, h)
        matches.append(centroid)
        cv2.circle(frame1,centroid, 5, (0,0,255), -1)
        ctdx,ctdy= get_centroid(x, y, w, h)
       
        for (x,y) in matches:
            if y<(line_y+offset) and y>(line_y-offset):
                cars=cars+1
                if(w>=60 ) and (h>=60):
                    crop = extra[y-int(h):y+int(h),x-int(w):x+int(w)]
                    #cv2.pyrUp(crop)
                    #cv2.pyrUp(crop)
                    cv2.imshow('cropped',crop)
                matches.remove((x,y))
                print(cars)
    cv2.drawContours(extra1,contours,-1,(0,0,255),2)            
    cv2.putText(frame1, "Total vehicle Detected: " + str(cars), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 170, 20), 2)

    cv2.putText(frame1, "B. Tech Project", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (210, 170, 0), 2)
    
    
    
    #cv2.drawContours(frame1,contours,-1,(0,0,255),2)


   # cv2.imshow('blur',closing)
    #cv2.imshow('gray',gray)
    cv2.imshow('back',bkgdsub)
    cv2.imshow("Difference" , thresh)
    cv2.imshow("contour", extra1)
    cv2.imshow("Original" , frame1)
    
    if cv2.waitKey(1) == 13:
        break
    frame1 = frame2
    ret , frame2 = cap.read()
#print(matches)    
cv2.destroyAllWindows()
cap.release()
