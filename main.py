import numpy as np;
import cvzone;
import cv2;
import pickle;


def checkParkingSpace(imgProcessed):
    availableSlots = 0;
    for pos in posList:
        x,y=pos;

        imgCrop=imgProcessed[y:y+height,x:x+width];
        # cv2.imshow(str(x*y),imgCrop);
        count=cv2.countNonZero(imgCrop);
        if count>1000:
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 0, 255), 2, 0)
            cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1,thickness=2,offset=0)
        elif count<900:
            availableSlots+=1;

            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 255, 0), 5, 2)
            cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0)
    cvzone.putTextRect(img, f'Available_Slots {availableSlots}/{len(posList)}', (100,60), scale=3, thickness=5, offset=20,border=2,font=cv2.FONT_HERSHEY_PLAIN)



cap=cv2.VideoCapture('carPark.mp4');
width,height=107,48;
with open('CarParkPos','rb')as f:
    posList=pickle.load(f);
while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0);

    ret, img = cap.read();
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY);
    imgBlur=cv2.GaussianBlur(imgGray,(3,3),1);
    imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16);
    imgMedian=cv2.medianBlur(imgThreshold,5);
    #for differentiating empty spaces;
    kernel=np.ones((3,3),np.uint8);
    imgdialate=cv2.dilate(imgMedian,kernel,iterations=1);

    checkParkingSpace(imgdialate);


    # for pos in posList:
    #     cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2,0)


    # cv2.imshow("imgmedian",imgMedian);
    # cv2.imshow("imgdialate",imgdialate);
    # cv2.imshow("Threshold",imgThreshold);
    cv2.imshow("Image",imgBlur);
    cv2.imshow("Image",img);

    cv2.waitKey(10);
