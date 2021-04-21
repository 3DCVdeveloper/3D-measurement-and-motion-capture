import json
import csv

keypointname=["Nose","Neck","RShoulder","RElbow","RWrist","LShoulder","LElbow","LWrist","MidHip","RHip",
              "RKnee","RAnkle","LHip","LKnee""LAnkle", "REye","LEye","REar","LEar","LBigToe","LSmallToe",
              "LHeel","RBigToe","RSmallToe","RHeel","Background"]

for i in range(2,14):
    inputfilename="json/col"+str(i)+"_keypoints.json"
    outputfilename="csv/col"+str(i)+"_keypoints.csv"
    with open(inputfilename,'r') as load_f:
        load_dict = json.load(load_f)
        print(load_dict)
    people=load_dict["people"]
    keypointlist=[]
    for i in people:
        for key,value in i.items():
            if key=="pose_keypoints_2d":
                for i in range(0, len(value), 3):
                    b = value[i:i + 3]
                    x=b[0]
                    y=b[1]
                    rightkeypoint=[keypointname[int(i/3)],x,y]
                    keypointlist.append(rightkeypoint)
    with open(outputfilename, 'w', newline='') as f:
        f_in = csv.writer(f)
        f_in.writerows(keypointlist)
    keypointlist.clear()