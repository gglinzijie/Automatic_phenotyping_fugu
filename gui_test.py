from picamera import PiCamera
from time import sleep
from guizero import App, Text, TextBox, PushButton,Picture
import numpy as np
import cv2
import glob

mtx = np.loadtxt("mtx.txt")
dist = np.loadtxt("dist.txt")

def calibra_save(file):
    img = cv2.imread(file)
    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    calname = 'cal' + file
    cv2.imwrite(calname , dst)
    calidone = calname + ' was saved!' 
    text.append(calidone)

camera = PiCamera()
camera.resolution = (800,480)
def streaming():
    camera.start_preview(fullscreen=False,
                         window = (500,80,320,260))
def stop_streaming():
    camera.stop_preview()
    
def photo():
    jpg_name = Individual.value + '.jpg'
    camera.capture(jpg_name, use_video_port=True)
    ok = jpg_name + ' was saved !'
    text.clear()
    text.append(ok)
    calibra_save(jpg_name)
    
    update_number = int(Individual.value) + 1
    Individual.clear()
    Individual.append(update_number)
    
    
app = App(title = "Fugu camera")
button_stream = PushButton(app, text = "stream",
                           command = streaming)
button_stop_stream = PushButton(app, text = "stop stream",
                           command = stop_streaming)
Individual = TextBox(app,"1")

snapshot = PushButton(app, text = "snapshot",
                      command = photo)
text = Text(app,text = '')

app.display()