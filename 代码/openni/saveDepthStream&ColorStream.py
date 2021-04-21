from openni import openni2
import numpy as np
import cv2

colp=r'E:\AoBi\data\test.avi'
depp=r'E:\AoBi\data\test.oni'

openni2.initialize()
dev = openni2.Device.open_any()
cap = cv2.VideoCapture(0)

#depthstream
depth_stream = dev.create_depth_stream()
depth_stream.start()

#initRecorder
rec = openni2.Recorder(depp.encode('utf8'))
rec.attach(depth_stream)
rec.start()

codec=cv2.VideoWriter_fourcc(*'MJPG')
fps=30.0
frameSize=(640,480)
out = cv2.VideoWriter(colp, codec, fps, frameSize)

while True:
    # getdepthframe
    depth_frame = depth_stream.read_frame()
    dframe_data = np.array(depth_frame.get_buffer_as_triplet()).reshape([480, 640, 2])
    dframe1 = np.asarray(dframe_data[:, :, 0], dtype='float32')
    dframe2 = np.asarray(dframe_data[:, :, 1], dtype='float32')
    dframe2 *= 255
    dframe = dframe1 + dframe2
    dframe = np.flipud(np.flip(dframe))
    cv2.imshow('depth', dframe)

    #getcolorframe
    ret, cframe = cap.read()
    out.write(cframe)
    cv2.imshow('frame',cframe)

    if cv2.waitKey(1) == ord('q'):
        break

depth_stream.stop()
rec.stop()
dev.close()
cv2.destroyAllWindows()




