## Introduction

This is a project for LiDAR to camera calibration， including automatic calibration and manual calibration.

## Prerequisites

- Cmake
- opencv 2.4
- eigen 3
- PCL 1.9
- Pangolin

## Compile
Compile in their respective folders

```shell
# mkdir build
mkdir -p build && cd build
# build
cmake .. && make
```

## Manual calibration tool

1. Four input files: 

   ```
   Usage: ./run_lidar2camera <image_path> <pcd_path> <intrinsic_json> <extrinsic_json>
   ```
+ **image_path:** image file from the Camera sensor
+ **pcd_path:** PCD file from the Lidar sensor
+ **intrinsic_json:** Camera intrinsic parameter JSON file
+ **extrinsic_json:** JSON file of initial values of extrinsic parameters between sensors
</br>


2. Run the test sample:

   The executable file is under the bin folder.

   ```
   cd ~./manual_calib/
   ./bin/run_lidar2camera data/0.jpg data/0.pcd data/center_camera-intrinsic.json data/top_center_lidar-to-center_camera-extrinsic.json
   ```

## Citation
This code is based on the research below:
```
@misc{2103.04558,
Author = {Tao Ma and Zhizheng Liu and Guohang Yan and Yikang Li},
Title = {CRLF: Automatic Calibration and Refinement based on Line Feature for LiDAR and Camera in Road Scenes},
Year = {2021},
Eprint = {arXiv:2103.04558},
}
   
```
