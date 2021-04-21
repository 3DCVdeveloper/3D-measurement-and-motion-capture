import numpy as np
import cv2

colimgp=r'E:\AoBi\data\body\color\col1.png'
xyzp=r'E:\AoBi\data\body\pointcloud\xyz\poi1.csv'
xyzrgbp=r'E:\AoBi\data\body\pointcloud\xyzrgb\rgbpoi1.csv'

colimg = cv2.imread(colimgp)
xyzpoi = np.loadtxt(xyzp, delimiter=',')

r = colimg[:, :, 2].reshape(307200, )
g = colimg[:, :, 1].reshape(307200, )
b = colimg[:, :, 0].reshape(307200, )
xyzrgbpoi = np.insert(np.insert(np.insert(xyzpoi, 3, values=r, axis=1), 4, values=g, axis=1), 5, values=b, axis=1)
np.savetxt(xyzrgbp, xyzrgbpoi, delimiter=',')

print("success!")



