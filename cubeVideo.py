import numpy as np
import cv2
import time
import glob

print 'start'

with np.load('B.npz') as X:
  mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

def draw(img, corners, imgpts):
  corner = tuple(corners[0].ravel())
  cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 2)
  cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 2)
  cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 2)
  return img

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

cap = cv2.VideoCapture(0)

while True
  img = cv2.imread(fname)
  ret, img = cap.read()
  img = cv2.flip(img,1)
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

  if ret == True:
    try:
      cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

      # Find the rotation and translation vectors.
      rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners, mtx, dist)

      #I can use np.arange(0.0, 8.0, 0.5)
      #for less size grid
      for z in xrange(-1,2):
        for y in xrange(-3,8):
          for x in xrange(8):
            axis =  np.float32([[-1+x,0+y,0+z], [-1+x,1+y,0+z], [0+x,1+y,0+z], [0+x,0+y,0+z],
                     [-1+x,0+y,-1+z],[-1+x,1+y,-1+z],[0+x,1+y,-1+z],[0+x,0+y,-1+z] ]) 
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
            img = drawCube(img,corners,imgpts,1)

    except:
      print 'error'
  else:
    print 'not found'

  img = cv2.resize(img,(768,576))
  cv2.imshow('img',img)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
  k = cv2.waitKey(700)
  #time.sleep(5)
cv2.destroyAllWindows()
# x y z