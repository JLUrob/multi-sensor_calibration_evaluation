## Introduction
This project is an implementation of the distortion evaluation proposed in our work.

## Prerequisites

#### Python
- opencv-python
- matplotlib

## Quick Start

```shell
# Calculate the length of edge
source calculate.sh
# Visualization results
source evaluate_dist.sh
```


## Data
<img src="./pic/Cameras/Camera_1/img/7.jpg" width="60%" height="60%" alt="Example of distorted image photography" div align=center /><br>

#### Data placement requirements
When aiming the camera at the calibration board to take photos, try to be perpendicular to the calibration board as much as possible, so that the calibration board is displayed symmetrically in the image.

<img src="../example_images/dist.png" width="60%" height="60%" alt="Example of distorted image photography" div align=center /><br>

## Results

#### Changes in row variance before and after orthodontic treatment

<img src="../results/picture/camera_dist/result_row.jpg" width="60%" height="60%" alt="Example of distorted image photography" div align=center /><br>

#### Changes in column variance before and after orthodontic treatment

<img src="../results/picture/camera_dist/result_col.jpg" width="60%" height="60%" alt="Example of distorted image photography" div align=center /><br>

#### Changes in the mean of row variance and column variance before and after orthodontic treatment
<img src="../results/picture/camera_dist//result_row_col.jpg" width="60%" height="60%" alt="Example of distorted image photography" div align=center /><br>


