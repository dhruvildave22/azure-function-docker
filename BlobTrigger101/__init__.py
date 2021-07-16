import logging

import azure.functions as func
import cv2
import numpy
import numpy as np
import csv

from pyzbar.pyzbar import decode


def main(myblob: func.InputStream):

    logging.info(f"It is done by dhruvil dave Python blob trigger function processed blob \n"
                                     f"Name: {myblob.name}\n"
                                     f"Blob Size: {myblob.length} bytes")

    video_input = f"https://qrcodestorageblob.blob.core.windows.net/{myblob.name}"
    print("video_inputvideo_inputvideo_inputvideo_inputvideo_inputvideo_input", video_input)
    found = set()
    cap = cv2.VideoCapture(video_input)
    qrcsv = "QR code link.csv"

    print("Cap", cap)
    i=0 #frame counter
    frameTime = 1 # time of each frame in ms, you can add logic to change this value.
    
    while(cap.isOpened()):
        ret = cap.grab()
        i=i+1 #increment counter

        if i % 10 == 0: # display only one tenth of the frames, you can change this parameter according to your needs
            if (ret != True):
                break

            ret, frame = cap.retrieve() #decode frame
            print("frame", frame)
            for barcode in decode(frame):
                myData = barcode.data.decode('utf-8')
                myDataType = barcode.type

                print(myData)

                milliseconds = cap.get(cv2.CAP_PROP_POS_MSEC)

                seconds = milliseconds//1000
                milliseconds = milliseconds%1000
                minutes = 0
                hours = 0
                if seconds >= 60:
                    minutes = seconds//60
                    seconds = seconds % 60

                if minutes >= 60:
                    hours = minutes//60
                    minutes = minutes % 60

                # Draw the barcode data and barcode type on the image
                printout = "{} ({})".format(myData, myDataType)

                startTimeStamp = f'{int(hours)}:{int(minutes)}:{int(seconds)}:{int(milliseconds)}'
                if myData not in found:
                    # Print barcode data and barcode type to the terminal
                    print("[INFO] Found {} barcode: {} timestamp: {}".format(myDataType, myData, startTimeStamp))
                    print(printout)

                    with open(qrcsv, 'a+',newline='') as f:  #newline=``No blank lines will appear
                        csv_write = csv.writer(f)
                        data = [myData, startTimeStamp]
                        csv_write.writerow(data)
                        print(data)

                        
                    
                    found.add(myData)

                print(startTimeStamp)
   
