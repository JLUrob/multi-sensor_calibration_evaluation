cd build
rm CMakeCache.txt
make -j8
cd ..
./bin/run_lidar2camera data/0.jpg data/0.pcd data/center_camera-intrinsic.json data/top_center_lidar-to-center_camera-extrinsic.json