import cv2
import numpy as np


def high_pass_filter(img):
    #use to detect edges of picture
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    rows=img.shape[0]
    cols=img.shape[1]
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

def sharpening(img,option):
    #credited to #fanbd for the idea
    #should change the kernel depends on what kind of image were dealing with
    kernel_1 = np.array([[-1, -1, -1],[-1, 9, -1],[-1, -1, -1]])
    kernel_2 = np.array([[1,1,1],[1,-4,1],[1,1,1]])
    kernel_3 = np.array([[1,1,1],[1,-9,1],[1,1,1]])
    kernel= np.ones((3,3))
    if option == 1:
        kernel = kernel_1
    elif option == 2:
        kernel = kernel_2
    elif option == 3:
        kernel = kernel_3
    sharp = cv2.filter2D(img, -1, kernel)
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    res = cv2.addWeighted(sharp, 1.5,blur , -0.5, 0)
    return res