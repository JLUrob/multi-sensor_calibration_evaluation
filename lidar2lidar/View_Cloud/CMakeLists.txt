cmake_minimum_required(VERSION 2.8.3)
project(cloud)
set(CMAKE_CXX_FLAGS "-std=c++11 -g -Wall")

find_package(PCL REQUIRED)
include_directories(${PCL_INCLUDE_DIRS})

find_package(Boost REQUIRED system)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)

file(GLOB_RECURSE PARSER_PATH src/*.cpp)
add_library(${PROJECT_NAME} STATIC ${PARSER_PATH})
target_link_libraries(${PROJECT_NAME} libjsoncpp.a ${OpenCV_LIBS} ${Boost_SYSTEM_LIBRARY})

add_executable(run_cloud src/cloud.cpp)
target_link_libraries(run_cloud ${PROJECT_NAME})
target_link_libraries(run_cloud ${PCL_LIBRARIES})
