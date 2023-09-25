 
#include <iostream> //标准输入输出流
#include <pcl/io/pcd_io.h> //PCL的PCD格式文件的输入输出头文件
#include <pcl/point_types.h> //PCL对各种格式的点的支持头文件
#include <pcl/visualization/cloud_viewer.h>
#include <string>
#include <vector>
using namespace std;

// int main(int argc, char* argv[])
// {
// 	string num = argv[1];
// 	string file_name = "../../Center_Points/center_points_" + num + ".txt";
// 	string pcd_name = "../../pcd/" + num + ".pcd";
// 	ifstream infile(file_name, ios::in);
// 	int n = 12;
// 	vector<float> datas(n);
// 	if(!infile.good()){
// 		return 0;
// 	}
// 	else{
		
// 		for(int i = 0; i < 12 ; i++){
// 			infile >> datas[i];
// 			// cout << datas[i] << endl;
// 		}
// 	}
// 	// return 0;
// 	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud1(new pcl::PointCloud<pcl::PointXYZ>); // 创建点云（指针）
// 	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud2(new pcl::PointCloud<pcl::PointXYZ>); // 创建点云（指针）
// 	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud3(new pcl::PointCloud<pcl::PointXYZ>); // 创建点云（指针）

// 	if (pcl::io::loadPCDFile<pcl::PointXYZ>(pcd_name, *cloud1) == -1) //* 读入PCD格式的文件，如果文件不存在，返回-1
// 	{
// 		PCL_ERROR("Couldn't read file test_pcd.pcd \n"); //文件不存在时，返回错误，终止程序。
// 		return (-1);
// 	}
// 	if (pcl::io::loadPCDFile<pcl::PointXYZ>(pcd_name, *cloud2) == -1) //* 读入PCD格式的文件，如果文件不存在，返回-1
// 	{
// 		PCL_ERROR("Couldn't read file test_pcd.pcd \n"); //文件不存在时，返回错误，终止程序。
// 		return (-1);
// 	}
// 	for(int i = 0; i < 4 ; i++){
// 		cloud2->points[i].x = datas[i*3];
// 		cloud2->points[i].y = datas[i*3+1];
// 		cloud2->points[i].z = datas[i*3+2];
// 		cout << cloud2->points[i] << endl;
// 	}
// 	*cloud3 = (*cloud1) + (*cloud2);
// 	// pcl::io::savePCDFILEASCII ("../../data/target_and_output_cloud.pcd", *cloud3);
//   // 初始化点云可视化界面
// 	pcl::visualization::CloudViewer viewer("pcd viewer");
// 	while(1){
// 		viewer.showCloud(cloud3);
// 	}

// 	system("pause");
// 	return (0);
// }


int main(int argc, char* argv[])
{
	if (argc != 2) {
    cout << "Usage: ./main camera_dir csv file"
                 "\nexample:\n\t"
                 "./singshow 10"
              << endl;
    return 0;
  }
	string num = argv[1];
	string file_name = "../../Center_Points/center_points_" + num + ".txt";
	string pcd_name = "../../pcd/" + num + ".pcd";
	ifstream infile(file_name, ios::in);
	int n = 12;
	vector<float> datas(n);
	if(!infile.good()){
		return 0;
	}
	else{
		
		for(int i = 0; i < 12 ; i++){
			infile >> datas[i];
			// cout << datas[i] << endl;
		}
	}
	// return 0;
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud1(new pcl::PointCloud<pcl::PointXYZ>); // 创建点云（指针）
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud2(new pcl::PointCloud<pcl::PointXYZ>); // 创建点云（指针）
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud3(new pcl::PointCloud<pcl::PointXYZ>); // 创建点云（指针）
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud4(new pcl::PointCloud<pcl::PointXYZ>); // 创建点云（指针）
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud5(new pcl::PointCloud<pcl::PointXYZ>); // 创建点云（指针）

	cloud2->width = 1;
  	cloud2->height = 1;
  	cloud2->is_dense = false;
  	cloud2->resize (cloud2->width * cloud2->height);

	cloud3->width = 1;
  	cloud3->height = 1;
  	cloud3->is_dense = false;
  	cloud3->resize (cloud3->width * cloud3->height);

	cloud4->width = 1;
  	cloud4->height = 1;
  	cloud4->is_dense = false;
  	cloud4->resize (cloud4->width * cloud4->height);

	cloud5->width = 1;
  	cloud5->height = 1;
  	cloud5->is_dense = false;
  	cloud5->resize (cloud5->width * cloud5->height);

	if (pcl::io::loadPCDFile<pcl::PointXYZ>(pcd_name, *cloud1) == -1) //* 读入PCD格式的文件，如果文件不存在，返回-1
	{
		PCL_ERROR("Couldn't read file test_pcd.pcd \n"); //文件不存在时，返回错误，终止程序。
		return (-1);
	}

	cloud2->points[0].x = datas[0];
	cloud2->points[0].y = datas[1];
	cloud2->points[0].z = datas[2];

	cloud3->points[0].x = datas[3];
	cloud3->points[0].y = datas[4];
	cloud3->points[0].z = datas[5];

	cloud4->points[0].x = datas[6];
	cloud4->points[0].y = datas[7];
	cloud4->points[0].z = datas[8];

	cloud5->points[0].x = datas[9];
	cloud5->points[0].y = datas[10];
	cloud5->points[0].z = datas[11];
	

	// 初始化点云可视化界面
	boost::shared_ptr<pcl::visualization::PCLVisualizer>
	viewer_final (new pcl::visualization::PCLVisualizer ("3D Viewer"));
	viewer_final->setBackgroundColor (0, 0, 0);

	//对点云着色（白色）并可视化
	pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ>
	cloud1_color (cloud1, 255, 255 ,255);
	viewer_final->addPointCloud<pcl::PointXYZ> (cloud1, cloud1_color, "cloud1");
	viewer_final->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE,
													1, "cloud1");

	//对左上角点着色（红色）并可视化
	pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ>
	cloud2_color (cloud2, 255, 0, 0);
	viewer_final->addPointCloud<pcl::PointXYZ> (cloud2, cloud2_color, "cloud2");
	viewer_final->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE,
													1, "cloud2");
													
	//对右上角点着色（绿色）并可视化
	pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ>
	cloud3_color (cloud3, 0, 255, 0);
	viewer_final->addPointCloud<pcl::PointXYZ> (cloud3, cloud3_color, "cloud3");
	viewer_final->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE,
													1, "cloud3");

	//对左下角点着色（蓝色）并可视化
	pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ>
	cloud4_color (cloud4, 0, 0, 255);
	viewer_final->addPointCloud<pcl::PointXYZ> (cloud4, cloud4_color, "cloud4");
	viewer_final->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE,
													1, "cloud4");

	//对右下角点着色（黄色）并可视化
	pcl::visualization::PointCloudColorHandlerCustom<pcl::PointXYZ>
	cloud5_color (cloud5, 255, 255, 0);
	viewer_final->addPointCloud<pcl::PointXYZ> (cloud5, cloud5_color, "cloud5");
	viewer_final->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE,
													1, "cloud5");
	// 启动可视化
	viewer_final->addCoordinateSystem (1.0);
	viewer_final->initCameraParameters ();
	//等待直到可视化窗口关闭。
	while (!viewer_final->wasStopped ())
	{
		viewer_final->spinOnce (100);
		boost::this_thread::sleep (boost::posix_time::microseconds (100000));
	}

	system("pause");
	return (0);
}