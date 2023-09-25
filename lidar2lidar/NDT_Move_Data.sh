# for example : source ICP_Move_Data.sh
cp ./Method/NDT_Space/transformed_data/room_scan1.pcd View_Cloud/data
cp ./Method/NDT_Space/transformed_data/room_scan2_transformed.pcd View_Cloud/data
cd View_Cloud/bin/
./run_cloud 1
./run_cloud 2
cd ../..
