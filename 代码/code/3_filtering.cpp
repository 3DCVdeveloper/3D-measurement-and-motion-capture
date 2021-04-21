//3_filtering.cpp
#include <iostream>
#include <fstream>
#include <sstream>
#include <pcl/point_types.h>
#include <pcl/common/common_headers.h>
#include <pcl/io/pcd_io.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <pcl/filters/passthrough.h>





int main()
{
    for (int filenum = 2; filenum < 14; filenum++)
    {
        //输入点云
        char pcd_file_name[200] = { 0 };
        sprintf(pcd_file_name, "%s%d%s", "F:\\orbbec\\openni\\pointcloud_result\\rgbpoi_body", filenum, ".pcd");
        //输出点云
        char pcd_result_file_name[200] = { 0 };
        sprintf(pcd_result_file_name, "%s%d%s", "F:\\orbbec\\openni\\pointcloud_result\\rgbpoi_body_filter", filenum, ".pcd");


        pcl::PointCloud<pcl::PointXYZRGB>::Ptr sourceCloud(new pcl::PointCloud<pcl::PointXYZRGB>);
        pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud_result(new pcl::PointCloud<pcl::PointXYZRGB>);


        if (pcl::io::loadPCDFile<pcl::PointXYZRGB>(pcd_file_name, *sourceCloud) == -1)
        {
            PCL_ERROR("Couldn't read file1 \n");
            return (-1);
        }
        std::cout << "Loaded " << sourceCloud->size() << " data points from file " << pcd_file_name << std::endl;

        //点云截取
        pcl::PassThrough<pcl::PointXYZRGB> pass;
        pass.setInputCloud(sourceCloud);
        pass.setFilterFieldName("x");
        pass.setFilterLimits(-280.0, 300.0);
        pass.filter(*cloud_result);
        std::cerr << "Cloud_x after filtering: " << std::endl;

        pass.setInputCloud(cloud_result);
        pass.setFilterFieldName("y");
        pass.setFilterLimits(-750.0, 830.0);
        pass.filter(*cloud_result);
        std::cerr << "Cloud_x after filtering: " << std::endl;

        pass.setInputCloud(cloud_result);
        pass.setFilterFieldName("z");
        pass.setFilterLimits(2200.0, 2800.0);
        pass.filter(*cloud_result);
        std::cerr << "Cloud_z after filtering: " << std::endl;


        pcl::io::savePCDFileASCII(pcd_result_file_name, *cloud_result);
        std::cerr << "Saved " << filenum << " " << cloud_result->size() << "changes result!" << std::endl;


    }


    return 0;
}










