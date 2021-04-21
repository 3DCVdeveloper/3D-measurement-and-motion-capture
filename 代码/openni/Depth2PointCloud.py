import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D\

depthp = r'E:\AoBi\data\weiyan_depth.csv'
poip = r'E:\AoBi\data\weiyan_point.csv'

## 从csv文件读取深度数据并显示深度图
depimg=np.genfromtxt(depthp, delimiter=',').astype(np.float32) #从CSV文件加载深度图数据
plt.imshow(np.clip(depimg,0.55,0.7),cmap='jet') #显示加载的深度图
plt.title('depth image')
plt.show()

## 从深度图img生成点云数据pc
## 生成点云使用的相机参数如下：
CAM_WID,CAM_HGT = 640,480   # 深度图img的图像尺寸
CAM_FX,CAM_FY = 598.088,599.855   # 相机的fx/fy参数
CAM_CX,CAM_CY = 316.466,237.723   # 相机的cx/cy参数
CAM_DVEC = np.array([-0.33354, 0.00924849, -0.000457208, -0.00215353, 0.0]) # 相机镜头的矫正参数，用于cv2.undistort()的输入之一

x, y = np.meshgrid(range(CAM_WID), range(CAM_HGT))
x = x.astype(np.float32) - CAM_CX
y = y.astype(np.float32) - CAM_CY

poi_z = depimg.copy()

poi_x = poi_z * x / CAM_FX  # X=Z*(u-cx)/fx
poi_y = poi_z * y / CAM_FY  # Y=Z*(v-cy)/fy
poi = np.array([poi_x.ravel(), poi_y.ravel(), poi_z.ravel()]).T

np.savetxt(poip, poi, fmt='%.18e', delimiter=',', newline='\n')  #将点云保存为csv文件
## 显示点云
poi=np.genfromtxt(poip, delimiter=',').astype(np.float32) # 从CSV文件加载点云
ax = plt.figure(1).gca(projection='3d')
ax.plot(poi[:,0],poi[:,1],poi[:,2],'b.',markersize=0.5)
plt.title('point cloud')
plt.show()

