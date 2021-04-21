//1_csv2pcd.cpp
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>

using namespace std;

typedef struct tagPOINT_3D
{
	double x;
	double y;
	double z;
	double r;
	double g;
	double b;
}POINT_WORLD;

vector<tagPOINT_3D> my_csvPoints;
tagPOINT_3D csvPoint;


int main()
{
	for (int filenum = 1; filenum < 14; filenum++)
	{
		//csv文件名称
		char csv_file_name[200] = { 0 };
		sprintf(csv_file_name, "%s%d%s", "F:\\orbbec\\openni\\pointcloud\\xyzrgb\\rgbpoi", filenum, ".csv");
		//pcd保存路径
		char pcd_file_name[200] = { 0 };
		sprintf(pcd_file_name, "%s%d%s", "F:\\orbbec\\openni\\pointcloud_pcd\\rgbpoi", filenum, ".pcd");

		//读取csv
		ifstream open_csv_file(csv_file_name);
		//读取csv的数据并提取
		string line;
		int i = 0;
		while (getline(open_csv_file, line))
		{

			istringstream sin(line);
			vector<string> fields;
			string field;
			while (getline(sin, field, ','))
			{
				fields.push_back(field);
			}
			if (i != 0) {
				csvPoint.x = atof(fields[0].c_str());
				csvPoint.y = atof(fields[1].c_str());
				csvPoint.z = atof(fields[2].c_str());
				csvPoint.r = atof(fields[3].c_str());
				csvPoint.g = atof(fields[4].c_str());
				csvPoint.b = atof(fields[5].c_str());
				my_csvPoints.push_back(csvPoint);
			}
			else
				i++;
			fields.clear();
		}

		pcl::PointCloud<pcl::PointXYZRGB> cloud;

		// 将csv中获取的点存到点云cloud
		cloud.width = my_csvPoints.size();
		cloud.height = 1;
		cloud.is_dense = false;
		cloud.points.resize(cloud.width * cloud.height);

		for (size_t i = 0; i < cloud.points.size(); ++i)
		{
			cloud.points[i].x = my_csvPoints[i].x;
			cloud.points[i].y = my_csvPoints[i].y;
			cloud.points[i].z = my_csvPoints[i].z;
			cloud.points[i].r = my_csvPoints[i].r;
			cloud.points[i].g = my_csvPoints[i].g;
			cloud.points[i].b = my_csvPoints[i].b;
		}

		pcl::io::savePCDFileASCII(pcd_file_name, cloud);
		std::cerr << "Saved " << filenum << " " << cloud.points.size() << " data points to csv2pcd.pcd." << std::endl;

		my_csvPoints.clear();

	}


	return 0;
}




