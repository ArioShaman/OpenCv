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

def drawCube(img, corners, imgpts):
  imgpts = np.int32(imgpts).reshape(-1,2)
  # draw ground floor in green
  cv2.drawContours(img, [imgpts[:4]],-1,(246, 171, 96),-3)

  # draw pillars in blue color
  for i,j in zip(range(4),range(4,8)):
    cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),1)

  # draw top layer in red color
  cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),1)
  return img

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

#this for simple axis
#axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

#this for cube
axis = np.float32([[0,0,0], [0,1,0], [1,1,0], [1,0,0],
                   [0,0,-1],[0,1,-1],[1,1,-1],[1,0,-1] ])

for fname in glob.glob('images/*.jpg'):
  img = cv2.imread(fname)
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

  if ret == True:
    try:
      cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

      # Find the rotation and translation vectors.
      rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners, mtx, dist)

      # project 3D points to image plane
      imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
      img = drawCube(img,corners,imgpts)
      cv2.imshow('img',img)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
      k = cv2.waitKey(350)
    except:
      print 'error'

cv2.destroyAllWindows()