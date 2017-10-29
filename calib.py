import numpy as np
import cv2
import time
import glob

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('images/*.jpg')

for fname in images:
  img = cv2.imread(fname)
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

  # Find the chess board corners
  ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

  # If found, add object points, image points (after refining them)
  if ret == True:
    try:
      objpoints.append(objp)

      cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
      imgpoints.append(corners)

      ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

      h,  w = img.shape[:2]
      newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
      dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

      x,y,w,h = roi
      dst = dst[y:y+h, x:x+w]

      ret, corners = cv2.findChessboardCorners(dst, (7,6),None)

      # Draw and display the corners
      cv2.drawChessboardCorners(dst, (7,6), corners,ret)
      cv2.imshow('img',dst)
      #time.sleep(1)
      cv2.waitKey(500)
    except:
      pass
cv2.destroyAllWindows()

np.savez('B.npz',mtx=mtx,dist=dist,rvecs=rvecs,tvecs=tvecs)
