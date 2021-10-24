"""
    Dinh Quoc Trung - 19020025

    Execute: 
        python3 gaussian_low.py <D0> <path_to_image_file>
            - D0: default = 30
            - path_to_image_file: default = "thor_ys.py" 
"""

import cv2
import sys
import numpy as np
from matplotlib import pyplot

def gauss2D_filter(shape=(3,3),sigma=0.5):
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

if __name__ == "__main__":
    # Get input D0 
    D0 = 30.0 
    if len(sys.argv) > 1:     
        D0 = float(sys.argv[1])
    print("D0 = " + str(D0))

    # Read image 
    path = "thor_ys.png"
    if len(sys.argv) > 2:
        path = sys.argv[2]
    print(path)
    img = cv2.imread(path, 0)

    # Transform using fft2
    f = np.fft.fft2(img)

    # Shift frequency coefs to center using fftshift
    fshift = np.fft.fftshift(f)

    # Create filter 
    mask = gauss2D_filter(fshift.shape, D0)

    # Filter in frequency domain
    img = fshift * mask

    # Shift frequency coefs back using ifftshift
    img = np.fft.ifftshift(img)

    # Invert transform using ifft2
    img = (np.fft.ifft2(img)).real

    # Show image     
    pyplot.imshow(img)
    pyplot.show()
