/*
 * Copyright (C) 2022 by Autonomous Driving Group, Shanghai AI Laboratory
 * Limited. All rights reserved.
 * Yan Guohang <yanguohang@pjlab.org.cn>
 */

#include <fstream>
#include <iostream>
#include <sstream>

#include "camera_calibrator.hpp"

int main(int argc, char **argv) {
  if (argc != 3) {
    std::cout << "Usage: ./main camera_dir csv file"
                 "\nexample:\n\t"
                 "./bin/lidar2camera data/intrinsic/ data/circle.csv"
              << std::endl;
    return 0;
  }

  std::string image_dir = argv[1];
  std::string csv_file = argv[2];
  std::cout << csv_file << std::endl;

  //读取雷达3d坐标 储存在lidar_3d_pts中
  std::ifstream fin(csv_file);
  std::string line;
  bool is_first = true;
  std::vector<std::vector<std::string>> lidar_3d_pts;
  while (getline(fin, line)) {
    // 跳过第一行
    if (is_first) {
      is_first = false;
      continue;
    }

    std::istringstream sin(line);
    std::vector<std::string> fields;
    std::string field;
    int i = 1;
    while (getline(sin, field, ',')) {
      fields.push_back(field);
      std::cout << "(" << i << "):" << field << " " ;
      i++;
    }
    std::cout << std::endl;
    lidar_3d_pts.push_back(fields);
  }

  //获取相机标定的图像(vec_mat)和图像路径(images_name)
  std::cout << image_dir << std::endl;
  std::vector<cv::String> images;
  cv::glob(image_dir, images);
  std::vector<cv::Mat> vec_mat;
  std::vector<std::string> images_name;
  for (const auto &path : images) {
    std::cout << path << std::endl;
    cv::Mat img = cv::imread(path, cv::IMREAD_GRAYSCALE); //图像灰度化
    vec_mat.push_back(img);
    images_name.push_back(path);
  }

  //开始联合标定
  //cv::{12, 8}棋盘格角矩阵大小
  //cv::{1920, 1080}图像分辨率
  CameraCalibrator m;
  cv::Mat camera_matrix = cv::Mat(3, 3, CV_32FC1, cv::Scalar::all(0));
  cv::Mat k = cv::Mat(1, 5, CV_32FC1, cv::Scalar::all(0));
  std::vector<cv::Mat> tvecsMat; 
  std::vector<cv::Mat> rvecsMat;
  m.set_input(images_name, vec_mat, cv::Size{12, 8}, lidar_3d_pts);
  m.get_result(camera_matrix, k, cv::Size{1920, 1080}, rvecsMat, tvecsMat);
  return 0;
}