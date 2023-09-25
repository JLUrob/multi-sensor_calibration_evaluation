cmake_minimum_required(VERSION 2.6)
project(singershow)
 
find_package(PCL 1.8 REQUIRED)
 
include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})
 
add_executable(singershow singershow.cpp)
 
target_link_libraries (singershow ${PCL_LIBRARIES})
 
install(TARGETS singershow RUNTIME DESTINATION bin)
