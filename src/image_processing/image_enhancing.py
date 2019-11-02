import cv2
import numpy as np
import matplotlib.pyplot as plt

def to_frequency_domain(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    magnitude_spectrum.astype("uint8")
    return magnitude_spectrum


def high_pass_filter(img):
    #use to detect edges of picture
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
    #ksize needs to be odd number
    res=cv2.GaussianBlur(img,(ksize,ksize),sigmaX=0)
    return res

def laplace(img):
    #a way to detect edges
    ksize=3
    ddepth=cv2.CV_16S
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(ksize,ksize),0)
    laplace=cv2.Laplacian(blur,ddepth,ksize=ksize)
    res=cv2.convertScaleAbs(laplace)
    return res

def log_transform(img):
    #  nothing to see here xd
    c = 255 / (np.log(1 + np.max(img)))
    log_transformed = c * np.log(1 + img)
    log_transformed = np.array(log_transformed, dtype=np.uint8)
    return log_transformed

def gamma_transform(img,gamma):
    #gamma should be between 0.1 and 3
    #gamma=1 is original picture
    gamma_corrected = np.array(255 * (img / 255) ** gamma, dtype='uint8')
    return gamma_corrected


def down_sampling(img,factor):
    #reduce number of pixels in image
    height=img.shape[0]
    length=img.shape[1]
    res = cv2.resize(img, (int(length /factor), int(height / factor)))
    res = cv2.resize(res, (length, height))
    return res

def to_negative(img):

    res=cv2.bitwise_not(img)
    return res

def intensity_slicing(img,min_range,max_range):
    #only map pixels in range, else is mapped 0
    height = img.shape[0]
    length = img.shape[1]
    for i in range(height):
        for j in range(length):
            if img[i, j] > min_range and img[i, j] < max_range:
                img[i, j] = 255
            else:
                img[i, j] = 0
    return img

def bit_plane_slicing(img,bit):
    #bit should be between 0 and 7
    plane = np.full((img.shape[0], img.shape[1]), 2 ** bit, np.uint8)
    res = cv2.bitwise_and(plane, img)
    res = res * 255
    return res

def sharpening(img,kernel):
    #credited to #fanbd for the idea
    #should change the kernel depends on what kind of image were dealing with
    # EX: kernel = np.array([[-1, -1, -1],[-1, 9, -1],[-1, -1, -1]])
    sharp = cv2.filter2D(img, -1, kernel)
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    res = cv2.addWeighted(sharp, 1.5,blur , -0.5, 0)
    return res
