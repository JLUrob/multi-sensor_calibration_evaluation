#include <pcl/io/pcd_io.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

typedef pcl::PointXYZRGBA PointT;
typedef pcl::PointCloud<PointT> PointCloudT;

// Mutex: //
boost::mutex cloud_mutex;
ofstream output_stream;  //(txt_name)
PointT point;

struct callback_args{
    // structure used to pass arguments to the callback function
    PointCloudT::Ptr clicked_points_3d;
    pcl::visualization::PCLVisualizer::Ptr viewerPtr;
};

void pp_callback(const pcl::visualization::PointPickingEvent& event, void* args)
{
    struct callback_args* data = (struct callback_args *)args;
    if (event.getPointIndex() == -1)
        return;
    PointT current_point;
    event.getPoint(current_point.x, current_point.y, current_point.z);
    data->clicked_points_3d->points.push_back(current_point);
    // Draw clicked points in red:
    pcl::visualization::PointCloudColorHandlerCustom<PointT> red(data->clicked_points_3d, 255, 0, 0);
    data->viewerPtr->removePointCloud("clicked_points");
    data->viewerPtr->addPointCloud(data->clicked_points_3d, red, "clicked_points");
    data->viewerPtr->setPointCloudRenderingProperties(pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 10, "clicked_points");
    std::cout << current_point.x << " " << current_point.y << " " << current_point.z << std::endl;
    point.x = current_point.x;
    point.y = current_point.y;
    point.z = current_point.z;
    output_stream << point.x << " " << point.y << " " << point.z << std::endl;
    // string f;
    // std::cout << "plase choose:" << std::endl;
    // std:: cout << "y(save)  n(not save)  q(end save)" << std::endl;
    // while(cin >> f){
    //     if(f == "y" || f == "n" || f == "q"|| f == "Y" || f == "N" || f == "Q"){
    //         if(f == "y" || f == "Y"){
    //             output_stream << point.x << " " << point.y << " " << point.z << std::endl;
    //         }
    //         if(f == "q" || f == "Q"){
    //             output_stream.close();
    //         } 
    //         break;
    //     }
    //     else{
    //         cout << "enter error!" <<endl;
    //     }
        
    // }
}

int main(int argc, char *argv[])
{
    if(argc != 2){
        std::cout << "error input !" << std::endl
                  << "example : " << "./run_cloud 10" << std::endl;
        return 0;
    }
    std::string file_id = argv[1];
    std::string filename = "../../pcd/" + file_id + ".pcd";

    string txt_name = "../../Points/points_" + file_id + ".txt";
    
    output_stream.open(txt_name);

    //visualizer
    pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>());
    boost::shared_ptr<pcl::visualization::PCLVisualizer> viewer(new pcl::visualization::PCLVisualizer("viewer"));

    if (pcl::io::loadPCDFile(filename, *cloud))
    {
        std::cerr << "ERROR: Cannot open file " << filename << "! Aborting..." << std::endl;
        return 0;
    }
    std::cout << cloud->points.size() << std::endl;

    //viewer->addPointCloud(cloud, "bunny");

    cloud_mutex.lock();    // for not overwriting the point cloud

    // Display pointcloud:
    viewer->addPointCloud(cloud, "bunny");
    viewer->setCameraPosition(0, 0, -20, 0, -10, 0, 0);

    // Add point picking callback to viewer:
    struct callback_args cb_args;
    PointCloudT::Ptr clicked_points_3d(new PointCloudT);
    cb_args.clicked_points_3d = clicked_points_3d;
    cb_args.viewerPtr = pcl::visualization::PCLVisualizer::Ptr(viewer);

    viewer->registerPointPickingCallback(pp_callback, (void*)&cb_args);

    std::cout << "Shift+click on three floor points, then press 'Q'..." << std::endl;
    // Spin until 'Q' is pressed:
    viewer->spin();
    // Close filestream
    output_stream.close();

    std::cout << "done." << std::endl;

    cloud_mutex.unlock();

    while (!viewer->wasStopped())
    {
        viewer->spinOnce(100);
        boost::this_thread::sleep(boost::posix_time::microseconds(100000));
    }
    return 0;
}