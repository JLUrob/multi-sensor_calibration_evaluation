cmake_minimum_required(VERSION 2.6)
project(show)
 
find_package(PCL 1.8 REQUIRED)
 
include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})
 
add_executable(show show.cpp)
 
target_link_libraries (show ${PCL_LIBRARIES})
 
# install(TARGETS show RUNTIME DESTINATION bin)
