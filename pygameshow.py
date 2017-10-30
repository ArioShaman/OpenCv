import pygame as pg
from pygame.locals import *
import cv2
import time
import numpy as np

filename = 'images/left15.jpg'

with np.load('B.npz') as X:
  mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

def drawCube(img, corners, imgpts,depth):
  gridColor = (255,53,85)
  imgpts = np.int32(imgpts).reshape(-1,2)  
  cv2.drawContours(img, [imgpts[:4]],-1, gridColor, depth)
  for i,j in zip(range(4),range(4,8)):
    cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),gridColor,depth)

  cv2.drawContours(img, [imgpts[4:]],-1,gridColor,depth)
  return img

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)


img = cv2.imread(filename)


gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, corners = cv2.findChessboardCorners(gray, (6,5),None)
print ret
try:  
  cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
  rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners, mtx, dist)
  for z in xrange(-1,2):
    for y in xrange(-2,6):
      for x in xrange(12):
        axis =  np.float32([[-1+x,0+y,0+z], [-1+x,1+y,0+z], [0+x,1+y,0+z], [0+x,0+y,0+z],
            [-1+x,0+y,-1+z],[-1+x,1+y,-1+z],[0+x,1+y,-1+z],[0+x,0+y,-1+z] ]) 
        imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
        img = drawCube(img,corners,imgpts,1)
except:
  img = gray

h, w = img.shape[:2]
img = pg.pixelcopy.make_surface(img)

pg.init()
screen = pg.display.set_mode((w,h))
img = pg.transform.rotate(img,-90)
img = pg.transform.flip(img,1,0)
done = False

while True:
  events = pg.event.get()
  for event in events:
    if event.type == KEYDOWN:
      event.mods = pg.key.get_mods()
      if event.key == K_ESCAPE:
        done = True
        pg.quit()
  screen.blit(img,(0,0))
  pg.display.flip()
