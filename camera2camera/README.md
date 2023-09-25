## Introduction
This project is an implementation of the camera2camera evaluation proposed in our work.

## Prerequisites

#### Python
- opencv-python
- matplotlib

## Quick Start

```shell
# Camera2Camera Calibrate
source calib.sh
# Visualization results
source Pic.sh
```


## Data

#### camera1 image
<img src="./datasets_2/camera1/01.jpg" width="60%" height="60%" alt="Example of distorted image photography" div align=center /><br>

#### camera2 image
<img src="./datasets_2/camera2/01.jpg" width="60%" height="60%" alt="Example of distorted image photography" div align=center /><br>

These photos of camera 1 and camera 2 with the same timestamp

#### Data placement requirements
Two cameras are placed in different positions, with fixed relative poses, and can collectively capture a checkerboard pattern.

## Results

#### Calibration results of two cameras

<img src="../results/camera2camera/datasets1/jpg_11/11.jpg" width="60%" height="60%" alt="Example of distorted image photography" div align=center /><br>

#### Distance error in camera coordinate system

<img src="../results/picture/camera2camera/result_distance.jpg" width="60%" height="60%" alt="Example of distorted image photography" div align=center /><br>

#### Angle error in camera coordinate system
<img src="../results/picture/camera2camera/result_theta.jpg" width="60%" height="60%" alt="Example of distorted image photography" div align=center /><br>

#### Average Reprojection Error in Pixel Coordinate System
<img src="../results/picture/camera2camera/result_reproject.jpg" width="60%" height="60%" alt="Example of distorted image photography" div align=center /><br>


