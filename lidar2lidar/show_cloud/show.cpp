#include <iostream>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/registration/ndt.h>
#include <pcl/filters/approximate_voxel_grid.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <boost/thread/thread.hpp>
#include <string>
using namespace std;

int main(int argc, char* argv[]){
  pcl::PointCloud<pcl::PointXYZ>::Ptr target_cloud (new pcl::PointCloud<pcl::PointXYZ>);
  //pcd文件的路径是相对可行性文件的路径
  string datasets = argv[1];
  string method = argv[2];
  string num = argv[3];
  string path1 = "../results/lidar2lidar/" + datasets + "/" + method + "/" + num + "/" + "room_scan1.pcd";
  string path2 = "../results/lidar2lidar/" + datasets + "/" + method + "/" + num + "/" + "room_scan2_transformed.pcd";
  if (pcl::io::loadPCDFile<pcl::PointXYZ> (path1, *target_cloud) == -1)
  {
    PCL_ERROR ("Couldn't read file room_scan1.pcd \n");
    return (-1);
  }
  std::cout << "Loaded " << target_cloud->size () << " data points from room_scan1.pcd" << std::endl;
  //加载从新视角得到的房间的第二次扫�?
  pcl::PointCloud<pcl::PointXYZ>::Ptr input_cloud (new pcl::PointCloud<pcl::PointXYZ>);
  if (pcl::io::loadPCDFile<pcl::PointXYZ> (path2, *input_cloud) == -1)
  {
    PCL_ERROR ("Couldn't read file room_scan2.pcd \n");
    return (-1);
  }
  // 初始化点云可视化界面
  boost::shared_ptr<pcl::visualization::PCLVisualizer>
  viewer_final (new pcl::visualization::PCLVisualizer ("3D Viewer"));
  viewer_final->setBackgroundColor (0, 0, 0);
  //对目标点云着色（红色）并可视�?
  pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ>
  target_color (target_cloud, 255, 0, 0);
  viewer_final->addPointCloud<pcl::PointXYZ> (target_cloud, target_color, "target cloud");
  viewer_final->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE,
                                                  1, "target cloud");
  //对转换后的目标点云着色（绿色）并可视�?
  pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ>
  output_color (input_cloud, 0, 255, 0);
  viewer_final->addPointCloud<pcl::PointXYZ> (input_cloud, output_color, "input cloud");
  viewer_final->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE,
                                                  1, "input cloud");                                                
  // 启动可视�?
  viewer_final->addCoordinateSystem (1.0);
  viewer_final->setCameraPosition(-4, -1, 3.8, 10, 3, -8, 0, 0, 1);
  // viewer_final->initCameraParameters ();
  
  //等待直到可视化窗口关闭�?
  while (!viewer_final->wasStopped ())
  {
    viewer_final->spinOnce (100);
    boost::this_thread::sleep (boost::posix_time::microseconds (100000));
  }
  return (0);    
}