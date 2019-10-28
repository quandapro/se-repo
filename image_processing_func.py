import cv2
import numpy as np
import matplotlib.pyplot as plt

#this file is only for testing.


def test(img):
    pass

img = cv2.imread('1.jpg', 0)
use_img = cv2.resize(img,(800,450))
# use_img=optimize_preprocess(use_img)
cv2.imshow("original",use_img)

res=spatial_enchance(use_img)
cv2.imshow("edited",res.astype('uint8'))
cv2.waitKey(0)
cv2.destroyAllWindows()



