from openni import openni2
import numpy as np
import cv2

oni_p=r'E:\AoBi\data\new.oni'
col_p=r'E:\AoBi\data\new.avi'

col_img_p=r'E:\AoBi\data\body\color\col'
dep_img_p=r'E:\AoBi\data\body\depth\img\dep'
dep_csv_p=r'E:\AoBi\data\body\depth\csv\dep'
poi_csv_p=r'E:\AoBi\data\body\pointcloud\xyz\poi'
rgbpoi_csv_p=r'E:\AoBi\data\body\pointcloud\xyzrgb\rgbpoi'

openni2.initialize()
dev = openni2.Device.open_any()
cap = cv2.VideoCapture(0)
# dev = openni2.Device.open_file(oni_p.encode('utf8'))
# cap = cv2.VideoCapture(col_p)

# depthStream
depth_stream = dev.create_depth_stream()
depth_stream.start()

CAM_WID, CAM_HGT = 640, 480  # 深度图img的图像尺寸
CAM_FX, CAM_FY = 598.088, 599.855  # 相机的fx/fy参数
CAM_CX, CAM_CY = 316.466, 237.723  # 相机的cx/cy参数
CAM_DVEC = np.array([-0.33354, 0.00924849, -0.000457208, -0.00215353, 0.0])  # 相机镜头的矫正参数，用于cv2.undistort()的输入之一
x, y = np.meshgrid(range(CAM_WID), range(CAM_HGT))
x = x.astype(np.float32) - CAM_CX
y = y.astype(np.float32) - CAM_CY

while True:
    # getDepthFrame
    depth_frame = depth_stream.read_frame()
    dframe_data = np.array(depth_frame.get_buffer_as_triplet()).reshape([480, 640, 2])
    dframe1 = np.asarray(dframe_data[:, :, 0], dtype='float32')
    dframe2 = np.asarray(dframe_data[:, :, 1], dtype='float32')
    dframe2 *= 255
    dframe = dframe1 + dframe2
    dframe = np.flipud(np.flip(dframe))
    cv2.imshow('depth', dframe)

    # getColorFrame
    ret, cframe = cap.read()
    cv2.imshow('color', cframe)

    key=cv2.waitKey(1)
    if key==ord('q'):
        num = input('第？张照片:')
        ##depth2pointcloud
        poi_z = dframe.copy()
        poi_x = poi_z * x / CAM_FX  # X=Z*(u-cx)/fx
        poi_y = poi_z * y / CAM_FY  # Y=Z*(v-cy)/fy
        poi = np.array([poi_x.ravel(), poi_y.ravel(), poi_z.ravel()]).T
        ##addRGB
        r = cframe[:, :, 2].reshape(307200, )
        g = cframe[:, :, 1].reshape(307200, )
        b = cframe[:, :, 0].reshape(307200, )
        rgbpoi = np.insert(np.insert(np.insert(poi, 3, values=r, axis=1), 4, values=g, axis=1), 5, values=b, axis=1)
        ##saveData
        cv2.imwrite(col_img_p + num + r'.png', cframe)  # saveColorImg
        cv2.imwrite(dep_img_p + num + r'.png', dframe)  # saveDepthImg
        np.savetxt(dep_csv_p + num + r'.csv', dframe, delimiter=',')  # 将深度数据存储到csv
        np.savetxt(poi_csv_p + num + r'.csv', poi, fmt='%.18e', delimiter=',', newline='\n')  # 将无色点云保存为csv文件
        np.savetxt(rgbpoi_csv_p + num + r'.csv', rgbpoi, delimiter=',') # 将彩色点云保存为csv文件
        print('NO.'+num+' success!')
        break

    elif key==ord('z'):
        break

depth_stream.stop()
dev.close()
cap.release()
cv2.destroyAllWindows()