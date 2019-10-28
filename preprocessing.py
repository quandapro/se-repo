import cv2
import numpy as np
def optimize_preprocess(img):
    #optimize picture before processing
    rows = img.shape[0]
    cols = img.shape[1]
    nrows = cv2.getOptimalDFTSize(rows)
    ncols = cv2.getOptimalDFTSize(cols)
    nimg=cv2.resize(img,(ncols,nrows))
    return nimg