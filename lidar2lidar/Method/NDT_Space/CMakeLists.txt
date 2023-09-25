cmake_minimum_required(VERSION 2.6)
project(test_ndt)
 
find_package(PCL 1.8 REQUIRED)
 
include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})
 
add_executable(test_ndt ndt.cpp)
 
target_link_libraries (test_ndt ${PCL_LIBRARIES})
 
install(TARGETS test_ndt RUNTIME DESTINATION bin)
