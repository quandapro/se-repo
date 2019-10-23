import cv2
import numpy as np
import matplotlib.pyplot as plt

def to_frequency_domain(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    return magnitude_spectrum


def high_pass_filter(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    rows, cols = img.shape
    crow, ccol = int(rows / 2), int(cols / 2)
    fw_size=100
    fshift[crow - int(fw_size/2):crow + int(fw_size/2), ccol - int(fw_size/2):ccol + int(fw_size/2)] = 0
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    return img_back
def gauss_blur(img,ksize):
    res=cv2.GaussianBlur(img,(ksize,ksize),sigmaX=0)
    return res

def log_transform(img):
    c = 255 / (np.log(1 + np.max(img)))
    log_transformed = c * np.log(1 + img)
    log_transformed = np.array(log_transformed, dtype=np.uint8)
    return log_transformed

def down_sampling(img,factor):
    height=img.shape[0]
    length=img.shape[1]
    res = cv2.resize(img, (int(length /factor), int(height / factor)))
    res = cv2.resize(res, (length, height))
    return res

def optimize_preprocess(img):
    rows, cols = img.shape
    nrows = cv2.getOptimalDFTSize(rows)
    ncols = cv2.getOptimalDFTSize(cols)
    nimg = np.zeros((nrows, ncols))
    nimg[:rows, :cols] = img
    return nimg

def test(img):
    height = img.shape[0]
    length = img.shape[1]
    for i in range(1,height):
        for j in range(1,length):
            if j%2==0:
                img[i][j]=img[i][j-1]
            if i%2==0:
                img[i][j]=img[i-1][j]
    return img

img = cv2.imread('1.jpg', 1)
img = cv2.resize(img,(800,450))
cv2.imshow("original",img)
res=log_transform(img)

cv2.imshow("edited",res)
cv2.waitKey(0)
cv2.destroyAllWindows()



