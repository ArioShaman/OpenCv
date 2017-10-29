import numpy as np
import cv2
import time
import glob

images = glob.glob('images/*.jpg')

img1 = cv2.imread(images[0])
img2 = cv2.imread(images[12])


vis = np.concatenate((img1, img2), axis=1)
#cv2.imwrite('out.png', vis)
cv2.imshow('img',vis)

cv2.waitKey(0)
cv2.destroyAllWindows()