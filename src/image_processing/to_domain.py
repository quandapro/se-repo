import cv2
import numpy as np

def to_frequency_domain(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    magnitude_spectrum.astype("uint8")
    return magnitude_spectrum

def gamma_transform(img,gamma):
    #gamma should be between 0.1 and 3
    #gamma=1 is original picture
    gamma_corrected = np.array(255 * (img / 255) ** gamma, dtype='uint8')
    return gamma_corrected

def to_negative(img):

    res=cv2.bitwise_not(img)
    return res

def log_transform(img):
    #  nothing to see here xd
    c = 255 / (np.log(1 + np.max(img)))
    log_transformed = c * np.log(1 + img)
    log_transformed = np.array(log_transformed, dtype=np.uint8)
    return log_transformed

