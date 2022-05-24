from __future__ import unicode_literals 
import os
from statistics import median
import sys
from cv2 import CV_32F
from sympy import isolate
try:
    import yt_dlp
except ModuleNotFoundError:
    if (str(input("Module yt_dlp missing. Install [Y,n]? ")).lower() == "n"):
        sys.exit("Module not installing. Exiting")
    os.system('pip install yt_dlp')
    import yt_dlp
try:
    import cv2
except ModuleNotFoundError:
    if (str(input("Module openCV missing. Install [Y,n]? ")).lower() == "n"):
        sys.exit("Module not installing. Exiting")
    os.system('pip install opencv-python')
    import yt_dlp
try:
    import numpy as np
except ModuleNotFoundError:
    if (str(input("Module numpy missing. Install [Y,n]? ")).lower() == "n"):
        sys.exit("Module not installing. Exiting")
    os.system('pip install numpy')
    import numpy as np


def download(youtubeID:str, downloadLocation:str, overwrite:bool=False):
    with os.scandir(downloadLocation) as it:
        for file in it:
            if file.is_file() and ''.join(str(file.name).split(".")[:-1]).endswith('[{0}]'.format(youtubeID)):
                if overwrite:
                    os.remove(file)
                elif (str(input("File exists. Overwrite [Y,n]? ")).lower() == "n"):
                    return
                else:
                    os.remove(file)
    ydl_opts = {'outtmpl': downloadLocation+'/%(title)s [{0}].%(ext)s'.format(youtubeID)}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com/watch?v={0}".format(youtubeID)])

def view(videoLocation:str,process:any,width:int, height:int, optional:dict={"skip_frames":1}):
    cap = cv2.VideoCapture(videoLocation)
    object_detector = cv2.createBackgroundSubtractorMOG2(history = 200, varThreshold = 40)
    cap.set(cv2.CAP_PROP_POS_FRAMES, optional["skip_frames"])
    while True:
        success, previous_frame = cap.read()
        success, frame = cap.read()
        if (process != None):
            frame = process(frame, width, height, optional = {"previous_frame":previous_frame,"object_detector":object_detector} | optional)
        cv2.imshow("Result", frame)
        if cv2.waitKey(25) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
def filter_blue(img, width, height, optional={"mask_only":False}):
    img = cv2.resize(img, (width, height))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90 , 90, 90])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    if optional["mask_only"]:
        return mask
    img = cv2.bitwise_and(img, img, mask = mask)
    return img
def filter_red(img, width, height, optional={"mask_only":False}):
    img = cv2.resize(img, (width, height))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([120 , 70, 50])
    upper_red = np.array([190, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    if optional["mask_only"]:
        return mask
    img = cv2.bitwise_and(img, img, mask = mask)
    return img
def filter_white(img, width, height, optional={}):
    img = cv2.resize(img, (width, height))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0 , 0, 168])
    upper_red = np.array([172,111,255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    img = cv2.bitwise_and(img, img, mask = mask)
    return img
def track_robot(img, width, height, optional={"filter_color":None,"background":None}):
    if (optional["filter_color"]!=None):
        color_filtered = optional["filter_color"](img, width, height, optional)
        optional["previous_frame"] = optional["filter_color"](optional["previous_frame"], width, height, optional)
    else:
        color_filtered = img
    img2 = remove_overlap(img, width, height, optional={"img_2":optional["background"]})
    blur = cv2.GaussianBlur(img2, (15, 15), cv2.IMREAD_UNCHANGED)
    _, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)
    return cv2.bitwise_and(img, img, mask=thresh)
def remove_overlap(img, width, height, optional={"img_2":False}):
    if (type(optional["img_2"]) != type(None)):
        gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(optional["img_2"],cv2.COLOR_BGR2GRAY)
        xor = cv2.bitwise_xor(gray1, gray2)
        _, thresh = cv2.threshold(xor, 90, 255, cv2.THRESH_BINARY) 
        return thresh
    return img
def extract_background(videoLocation:str, startFrame:int=0, frameFromEnd:int=0, width:int=0, height:int=0):
    cap = cv2.VideoCapture(videoLocation)
    frameIds = (cap.get(cv2.CAP_PROP_FRAME_COUNT) - startFrame - frameFromEnd) * np.random.uniform(size=100)
    frames=[]
    for id in frameIds:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(id+startFrame))
        ret, frame = cap.read()
        frames.append(frame)  
    medianFrame = np.median(frames, axis=0).astype(dtype=np.uint8)
    return medianFrame
#download("-RYGCu0ysw8","./Match/Downloads")
background = extract_background("./Qualification 22 - 2022 FIRST Championship - Turing Division [-RYGCu0ysw8].mp4", 1000,500,1280,720)
view("./Qualification 22 - 2022 FIRST Championship - Turing Division [-RYGCu0ysw8].mp4",track_robot,1280,720, optional={"filter_color":None,"background":background, "skip_frames":110})
