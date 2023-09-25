#include <iostream>  
#include <string>  
#include <pcl/io/ply_io.h>  //ply文件读取头文件
#include <pcl/point_types.h>  
#include <pcl/registration/icp.h> //配准所需头文件 
#include <pcl/visualization/pcl_visualizer.h>  //可视化所需头文件
#include <pcl/console/time.h>   // TicToc  //头文件计时
#include <pcl/io/pcd_io.h>//pcd文件读取
#include <pcl/filters/voxel_grid.h>//体素降采样滤波

typedef pcl::PointXYZ PointT;
typedef pcl::PointCloud<PointT> PointCloudT;
bool next_iteration = false;//迭代flag
bool if_or_save = false;//是否保存当前点云

//打印矩阵函数
void print4x4Matrix(const Eigen::Matrix4d& matrix)
{
	printf("Rotation matrix :\n");
	printf("    | %6.5f %6.5f %6.5f | \n", matrix(0, 0), matrix(0, 1), matrix(0, 2));
	printf("R = | %6.5f %6.5f %6.5f | \n", matrix(1, 0), matrix(1, 1), matrix(1, 2));
	printf("    | %6.5f %6.5f %6.5f | \n", matrix(2, 0), matrix(2, 1), matrix(2, 2));
	printf("Translation vector :\n");
	printf("t = < %6.5f, %6.5f, %6.5f >\n\n", matrix(0, 3), matrix(1, 3), matrix(2, 3));
}

//键盘回调函数
void keyboardEventOccurred(const pcl::visualization::KeyboardEvent& event, void* nothing)
{
	//如果按下空格键，next_iteration=true
	if (event.getKeySym() == "space" && event.keyDown())
		next_iteration = true;
    if (event.getKeySym() == "s" && event.keyDown())
        if_or_save = true;
}

int main()
{
	 //定义需要用到的点云（读入的，转换的，ICP调整的三个点云） 
	PointCloudT::Ptr cloud_in_tgt(new PointCloudT);  // Original point cloud  （目标点云）
    PointCloudT::Ptr cloud_in_toberegistration(new PointCloudT);  // Original point cloud  （从文件读取待配准的点云）
	PointCloudT::Ptr cloud_toberegistration(new PointCloudT);  // Transformed point cloud	待配准的点云
	PointCloudT::Ptr cloud_icp_in(new PointCloudT);   //filtered and icp input point cloud 经预处理后传入icp算法的目标点云
	PointCloudT::Ptr cloud_icp_toberegistration(new PointCloudT);  //filtered and icp output point cloud   经预处理后传入icp算法的待配准点云

	//时差=time.tok-time.tic 用于计时
	pcl::console::TicToc time;
	time.tic();
	std::string filename1 = "../data/room_scan1.pcd";//点云文件名
	if (pcl::io::loadPCDFile<pcl::PointXYZ>(filename1, *cloud_in_tgt) == -1)//*打开点云文件	
	{
		PCL_ERROR("Couldn't read file test_pcd.pcd\n");//输出错误原因：读取文件失败
		return(-1);//程序结束
	}
    //输出读取点云的点数与点云读取时间
	std::cout << "\nLoaded file " << filename1 << " (" << cloud_in_tgt->size() << " points) in " << time.toc() << " ms\n" << std::endl;
    
    std::string filename2 = "../data/room_scan2.pcd";//点云文件名
	if (pcl::io::loadPCDFile<pcl::PointXYZ>(filename2, *cloud_in_toberegistration) == -1)//*打开点云文件	
	{
		PCL_ERROR("Couldn't read file test_pcd.pcd\n");//输出错误原因：读取文件失败
		return(-1);//程序结束
	}
	//输出读取点云的点数与点云读取时间
	std::cout << "\nLoaded file " << filename2 << " (" << cloud_in_toberegistration->size() << " points) in " << time.toc() << " ms\n" << std::endl;
    
	/*将读取的点云复制，以提供配准传入的参数以及多个可视化窗口的显示
	* cloud_icp_in将作为icp算法的目标点云参数传入
	* cloud_toberegistration是icp算法的源点云（待配准点云）
	*/

    
	*cloud_icp_in = *cloud_in_tgt;
    *cloud_toberegistration = *cloud_in_toberegistration;
	// *cloud_toberegistration = *cloud_in_tgt;

	//体素降采样滤波
	pcl::VoxelGrid<pcl::PointXYZ> voxel_grid;//创建滤波器对象
	voxel_grid.setLeafSize(0.01, 0.01, 0.01);//设置体素大小
	voxel_grid.setInputCloud(cloud_in_tgt);//输入待降采样的点云
	voxel_grid.filter(*cloud_icp_in);//降采样后放入cloud_icp_in
	std::cout << "down size *cloud_in_tgt to" << cloud_icp_in->size() << endl;
	//同理将另一个点云降采样
	voxel_grid.setInputCloud(cloud_toberegistration);
	voxel_grid.filter(*cloud_icp_toberegistration);
	std::cout << "down size *cloud_toberegistration to" << cloud_icp_toberegistration->size() << endl;

	// // 定义旋转平移的转换矩阵
	// Eigen::Matrix4d transformation_matrix = Eigen::Matrix4d::Identity();
	// // A rotation matrix (see https://en.wikipedia.org/wiki/Rotation_matrix)  
	// double theta = M_PI / 4;  // The angle of rotation in radians 
	// transformation_matrix(0, 0) = cos(theta);
	// transformation_matrix(0, 1) = -sin(theta);
	// transformation_matrix(1, 0) = sin(theta);
	// transformation_matrix(1, 1) = cos(theta);
	// //Z轴平移0.4米
	//  //A translation on Z axis (0.4 meters)  
	// transformation_matrix(2, 3) = 0.0;
	// //打印出旋转矩阵R和平移T
	// std::cout << "Applying this rigid transformation to: cloud_in -> cloud_icp" << std::endl;
	// print4x4Matrix(transformation_matrix);
	// std::cout << std::endl << std::endl << std::endl;

	// //用矩阵transformation_matrix将点云进行空间变换，得到的点云和目标点云间就有了空间的旋转平移关系，后面使用icp算法将其配准还原
	// pcl::transformPointCloud(*cloud_toberegistration, *cloud_toberegistration, transformation_matrix);
	// pcl::transformPointCloud(*cloud_icp_toberegistration, *cloud_icp_toberegistration, transformation_matrix);

	// Visualization 可视化 
	pcl::visualization::PCLVisualizer viewer("ICP demo");//窗口标题
	// Create two vertically separated viewports  
	int v1(0);//设置4个小窗口
	int v2(1);
	int v3(2);
	int v4(3);
	//设置小窗口的位置分布
	viewer.createViewPort(0.0, 0.5, 0.5, 1.0, v1);
	viewer.createViewPort(0.5, 0.5, 1.0, 1.0, v2);
	viewer.createViewPort(0.0, 0.0, 0.5, 0.5, v3);
	viewer.createViewPort(0.5, 0.0, 1.0, 0.5, v4);
	// The color we will be using  
	float bckgr_gray_level = 0.0;  // Black  黑
	float txt_gray_lvl = 1.0 - bckgr_gray_level;//文本颜色与背景相反

	viewer.addCoordinateSystem(1.0);//设置坐标轴，1.0是坐标轴的可视大小
	// Original point cloud is white  目标点云设置为白色
	pcl::visualization::PointCloudColorHandlerCustom<PointT> cloud_in_color_h(cloud_in_tgt, (int)255 * txt_gray_lvl, (int)255 * txt_gray_lvl, (int)255 * txt_gray_lvl);
	//在3个窗口中添加目标点云，目标点云在可视化的过程中是不会动的
	viewer.addPointCloud(cloud_in_tgt, cloud_in_color_h, "cloud_in_v1", v1);//显示cloud_in_tgt第一次的点云
	viewer.addPointCloud(cloud_in_tgt, cloud_in_color_h, "cloud_in_v2", v2);
	viewer.addPointCloud(cloud_icp_in, cloud_in_color_h, "cloud_in_v3", v3);

	//Transformed point cloud is green  经目标点云旋转平移后并且未降采样的点云设置为绿色，放在窗口1中
	pcl::visualization::PointCloudColorHandlerCustom<PointT> cloud_tr_color_h(cloud_toberegistration, 20, 180, 20);
	viewer.addPointCloud(cloud_toberegistration, cloud_tr_color_h, "cloud_tr_v1", v1);

	// ICP aligned point cloud is red  经旋转平移后未降采样的点云设置为红色，放在窗口2，后面将随着迭代过程更新
	pcl::visualization::PointCloudColorHandlerCustom<PointT> cloud_icp_color_h(cloud_toberegistration, 180, 20, 20);
	viewer.addPointCloud(cloud_toberegistration, cloud_icp_color_h, "cloud_icp_v2", v2);

	// //ICP aligned point cloud is red  旋转平移并降采样的点云设置为红色，放在窗口3，用于icp的输入，并随着迭代过程更新位置
	viewer.addPointCloud(cloud_icp_toberegistration, cloud_icp_color_h, "cloud_icp_v3", v3);

	//Adding text descriptions in each viewport  添加文字信息
	viewer.addText("White: Original point cloud\nGreen: Matrix transformed point cloud", 10, 15, 16, txt_gray_lvl, txt_gray_lvl, txt_gray_lvl, "icp_info_1", v1);
	viewer.addText("White: Original point cloud\nRed: ICP aligned point cloud", 10, 15, 16, txt_gray_lvl, txt_gray_lvl, txt_gray_lvl, "icp_info_2", v2);

	/*icp迭代次数iterations设置为1时，算法执行一次迭代。算法内部是先执行一次迭代再判定当前迭代次数是否大于等于设定次数*/
	int iterations = 1;  // Default number of ICP iterations  icp迭代次数，设为1
	std::stringstream ss;
	ss << iterations;
	std::string iterations_cnt = "ICP iterations = " + ss.str();//显示算法已经迭代了多少次
	viewer.addText(iterations_cnt, 10, 60, 16, txt_gray_lvl, txt_gray_lvl, txt_gray_lvl, "iterations_cnt", v2);
	viewer.addText("Zhiyang Wang", 10, 80, 16, txt_gray_lvl, txt_gray_lvl, txt_gray_lvl, "author", v2);

	//Set background color  设置背景颜色，上面已设定bckgr_gray_level=0.0，所以背景全黑
	viewer.setBackgroundColor(bckgr_gray_level, bckgr_gray_level, bckgr_gray_level, v1);
	viewer.setBackgroundColor(bckgr_gray_level, bckgr_gray_level, bckgr_gray_level, v2);
	viewer.setBackgroundColor(bckgr_gray_level, bckgr_gray_level, bckgr_gray_level, v3);

	//Set camera position and orientation  设置可视化窗口的初始视角
	viewer.setCameraPosition(-3.68332, 2.94092, 5.71266, 0.289847, 0.921947, -0.256907, 0);
	viewer.setSize(1280, 1024);  // Visualiser window size  设置整个可视化窗口大小  

	 //Register keyboard callback :  //键盘回调函数，响应键盘输入
	viewer.registerKeyboardCallback(&keyboardEventOccurred, (void*)NULL);

	// The Iterative Closest Point algorithm  icp算法开始
	time.tic();
	pcl::IterativeClosestPoint<PointT, PointT> icp;
	icp.setMaximumIterations(iterations);//设置最大迭代次数，iterations在上面已经设置为0，即只使用一次icp算法
	icp.setInputSource(cloud_icp_toberegistration);//输入目标点云，是原读取的目标点云只经过降采样后的点云
	icp.setInputTarget(cloud_icp_in);//输入待配准点云，是原读取的目标点云经旋转平移并降采样后的点云
	icp.align(*cloud_icp_toberegistration);//经1次icp算法配准后的点云

	Eigen::Matrix4f icp_trans;
	icp_trans = icp.getFinalTransformation();//获取当前求解的旋转平移矩阵
	std::cout << endl;
	//使用得到的变换对未降采样的点云进行变换，以达到显示效果
	pcl::transformPointCloud(*cloud_toberegistration, *cloud_toberegistration, icp_trans);
	// We set this variable to 1 for the next time we will call .align () function  设置迭代次数为1，下一次使用键盘交互来完成一次迭代
	icp.setMaximumIterations(1);    
	std::cout << "Applied " << iterations << " ICP iteration(s) in " << time.toc() << " ms" << std::endl;

	if (icp.hasConverged())//算法是否正常收敛
	{
		std::cout << "\nICP has converged, score is " << icp.getFitnessScore() << std::endl;//算法的mse（均方误差）
		std::cout << "\nICP transformation " << iterations << " : cloud_icp -> cloud_in" << std::endl;
		std::cout << endl << endl << endl;
	}
	else
	{
		//若不是则输出错误并停止
		PCL_ERROR("\nICP has not converged.\n");
		system("pause");
		return (-1);
	}
	//在2、3窗口更新上次经icp算法后的点云，这个地方注意看，之前是addpointcloud添加点云，这里是updatePointCloud是更新之前添加好的点云
	viewer.updatePointCloud(cloud_toberegistration, cloud_icp_color_h, "cloud_icp_v2");
	viewer.updatePointCloud(cloud_icp_toberegistration, cloud_icp_color_h, "cloud_icp_v3");

	//Display the visualiser  
	while (!viewer.wasStopped())
	{
		viewer.spinOnce();
		// The user pressed "space" :  当键盘按下空格键，next_iteration变为true（见最上面的键盘回调函数代码），if里面的语句执行
        if (if_or_save)
        {
            pcl::io::savePCDFileASCII ("../transformed_data/room_scan2_transformed.pcd", *cloud_icp_toberegistration);
        }
		if (next_iteration)
		{
			// The Iterative Closest Point algorithm  
			time.tic();
			icp.align(*cloud_icp_toberegistration);//将上一次配准后的点云作为输入，进行下一次配准
			std::cout << "Applied 1 ICP iteration in " << time.toc() << " ms" << std::endl;

			icp_trans = icp.getFinalTransformation();
			std::cout << "trans matrix:\n " << /*icp_transdisplay**/icp_trans << endl;

			std::cout << endl;
			//使用创建的变换对过滤及未过滤的输入点云进行变换
			pcl::transformPointCloud(*cloud_toberegistration, *cloud_toberegistration, icp_trans);

			if (icp.hasConverged())
			{
				printf("\033[11A");  // Go up 11 lines in terminal output.  
				printf("\nICP has converged, score is %+.0e\n", icp.getFitnessScore());
				std::cout << "\nICP transformation " << ++iterations << " : cloud_icp -> cloud_in" << std::endl;
				std::cout << endl << endl << endl;
				//更新显示信息与点云
				ss.str("");
				ss << iterations;
				std::string iterations_cnt = "ICP iterations = " + ss.str();
				viewer.updateText(iterations_cnt, 10, 60, 16, txt_gray_lvl, txt_gray_lvl, txt_gray_lvl, "iterations_cnt");
				viewer.updatePointCloud(cloud_toberegistration, cloud_icp_color_h, "cloud_icp_v2");
				viewer.updatePointCloud(cloud_icp_toberegistration, cloud_icp_color_h, "cloud_icp_v3");
			}
			else
			{
				PCL_ERROR("\nICP has not converged.\n");
				system("pause");
				return (-1);
			}
		}
		next_iteration = false;//next_iteration设为false，等再次按下空格键时next_iteration=true再进行配准
        if_or_save = false;
	}
	system("pause");
	return (0);
}

