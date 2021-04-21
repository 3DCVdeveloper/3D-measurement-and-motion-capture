//2_change_detection.cpp

#include <iostream>
#include <fstream>
#include <sstream>
#include <pcl/point_types.h>
#include <pcl/common/common_headers.h>
#include <pcl/io/pcd_io.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <pcl/point_cloud.h>
#include <pcl/octree/octree_pointcloud_changedetector.h>
#include <vector>
#include <ctime>





int main()
{
	for (int filenum = 2; filenum < 14; filenum++)
	{
		//��������
		char pcd_origin_file_name[200] = { 0 };
		sprintf(pcd_origin_file_name, "%s%d%s", "F:\\orbbec\\openni\\pointcloud_pcd\\rgbpoi", 1, ".pcd");
		//���������
		char pcd_change_file_name[200] = { 0 };
		sprintf(pcd_change_file_name, "%s%d%s", "F:\\orbbec\\openni\\pointcloud_pcd\\rgbpoi", filenum, ".pcd");
		//���������
		char pcd_result_file_name[200] = { 0 };
		sprintf(pcd_result_file_name, "%s%d%s", "F:\\orbbec\\openni\\pointcloud_result\\rgbpoi_body", filenum, ".pcd");


		pcl::PointCloud<pcl::PointXYZRGB>::Ptr sourceCloud(new pcl::PointCloud<pcl::PointXYZRGB>);//��������
		pcl::PointCloud<pcl::PointXYZRGB>::Ptr handledCloud(new pcl::PointCloud<pcl::PointXYZRGB>);//���������仯�ĵ���


		if (pcl::io::loadPCDFile<pcl::PointXYZRGB>(pcd_origin_file_name, *sourceCloud) == -1)
		{
			PCL_ERROR("Couldn't read file1 \n");
			return (-1);
		}
		std::cout << "Loaded " << sourceCloud->size() << " data points from file " << pcd_origin_file_name << std::endl;


		if (pcl::io::loadPCDFile<pcl::PointXYZRGB>(pcd_change_file_name, *handledCloud) == -1)
		{
			PCL_ERROR("Couldn't read file2 \n");
			return (-1);
		}
		std::cout << "Loaded " << handledCloud->size() << " data points from file " << pcd_change_file_name << std::endl;


		float resolution = 50.0f;//�ֱ��ʣ���λΪ����


		pcl::octree::OctreePointCloudChangeDetector<pcl::PointXYZRGB> octree(resolution);
		octree.setInputCloud(sourceCloud);//�������
		octree.addPointsFromInputCloud();//��������ƹ����˲���
		octree.switchBuffers();//�����˲�������

		octree.setInputCloud(handledCloud);//�仯�����
		octree.addPointsFromInputCloud();

		std::vector<int> newPointIdxVector;//�洢�¼ӵ������������


		octree.getPointIndicesFromNewVoxels(newPointIdxVector);//��ȡ�����������

		//��������ķŵ�cloud_result��ָ����ڴ���
		pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud_result(new pcl::PointCloud<pcl::PointXYZRGB>);

		cloud_result->width = newPointIdxVector.size();
		cloud_result->height = 1;
		cloud_result->is_dense = false;
		cloud_result->points.resize(cloud_result->width * cloud_result->height);
		for (size_t i = 0; i < newPointIdxVector.size(); ++i)
		{
			cloud_result->points[i].x = handledCloud->points[newPointIdxVector[i]].x;
			cloud_result->points[i].y = handledCloud->points[newPointIdxVector[i]].y;
			cloud_result->points[i].z = handledCloud->points[newPointIdxVector[i]].z;
			cloud_result->points[i].r = handledCloud->points[newPointIdxVector[i]].r;
			cloud_result->points[i].g = handledCloud->points[newPointIdxVector[i]].g;
			cloud_result->points[i].a = handledCloud->points[newPointIdxVector[i]].b;
		}


		pcl::io::savePCDFileASCII(pcd_result_file_name, *cloud_result);
		std::cerr << "Saved " << filenum << " " << cloud_result->size() << "changes result!" << std::endl;

	}




	return 0;
}








