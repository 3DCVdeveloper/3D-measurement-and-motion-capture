from openni import openni2
import numpy as np
import cv2

path=r'E:\AoBi\data\test.oni'

openni2.initialize()
# dev = openni2.Device.open_any()
dev = openni2.Device.open_file(path.encode('utf8')) #读取oni文件

depth_stream = dev.create_depth_stream()
depth_stream.start()

cv2.namedWindow('depth')

while True:
    depth_frame = depth_stream.read_frame()
    dframe_data = np.array(depth_frame.get_buffer_as_triplet()).reshape([480, 640, 2])
    dframe1 = np.asarray(dframe_data[:, :, 0], dtype='float32')
    dframe2 = np.asarray(dframe_data[:, :, 1], dtype='float32')
    dframe2 *= 255
    dframe = dframe1 + dframe2
    dframe = np.flipud(np.flip(dframe))

    cv2.imshow('depth', dframe)

    key = cv2.waitKey(1)
    if int(key) == ord('q'):
        break

depth_stream.stop()
dev.close()
