# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "/home/jlurobot/Desktop/Camera calibration/View_Cloud/lidar2camera/View_Cloud"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "/home/jlurobot/Desktop/Camera calibration/View_Cloud/lidar2camera/View_Cloud/build"

# Include any dependencies generated for this target.
include CMakeFiles/cloud.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/cloud.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/cloud.dir/flags.make

CMakeFiles/cloud.dir/src/cloud.cpp.o: CMakeFiles/cloud.dir/flags.make
CMakeFiles/cloud.dir/src/cloud.cpp.o: ../src/cloud.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/home/jlurobot/Desktop/Camera calibration/View_Cloud/lidar2camera/View_Cloud/build/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/cloud.dir/src/cloud.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/cloud.dir/src/cloud.cpp.o -c "/home/jlurobot/Desktop/Camera calibration/View_Cloud/lidar2camera/View_Cloud/src/cloud.cpp"

CMakeFiles/cloud.dir/src/cloud.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/cloud.dir/src/cloud.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E "/home/jlurobot/Desktop/Camera calibration/View_Cloud/lidar2camera/View_Cloud/src/cloud.cpp" > CMakeFiles/cloud.dir/src/cloud.cpp.i

CMakeFiles/cloud.dir/src/cloud.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/cloud.dir/src/cloud.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S "/home/jlurobot/Desktop/Camera calibration/View_Cloud/lidar2camera/View_Cloud/src/cloud.cpp" -o CMakeFiles/cloud.dir/src/cloud.cpp.s

CMakeFiles/cloud.dir/src/cloud.cpp.o.requires:

.PHONY : CMakeFiles/cloud.dir/src/cloud.cpp.o.requires

CMakeFiles/cloud.dir/src/cloud.cpp.o.provides: CMakeFiles/cloud.dir/src/cloud.cpp.o.requires
	$(MAKE) -f CMakeFiles/cloud.dir/build.make CMakeFiles/cloud.dir/src/cloud.cpp.o.provides.build
.PHONY : CMakeFiles/cloud.dir/src/cloud.cpp.o.provides

CMakeFiles/cloud.dir/src/cloud.cpp.o.provides.build: CMakeFiles/cloud.dir/src/cloud.cpp.o


# Object files for target cloud
cloud_OBJECTS = \
"CMakeFiles/cloud.dir/src/cloud.cpp.o"

# External object files for target cloud
cloud_EXTERNAL_OBJECTS =

../lib/libcloud.a: CMakeFiles/cloud.dir/src/cloud.cpp.o
../lib/libcloud.a: CMakeFiles/cloud.dir/build.make
../lib/libcloud.a: CMakeFiles/cloud.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="/home/jlurobot/Desktop/Camera calibration/View_Cloud/lidar2camera/View_Cloud/build/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library ../lib/libcloud.a"
	$(CMAKE_COMMAND) -P CMakeFiles/cloud.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/cloud.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/cloud.dir/build: ../lib/libcloud.a

.PHONY : CMakeFiles/cloud.dir/build

CMakeFiles/cloud.dir/requires: CMakeFiles/cloud.dir/src/cloud.cpp.o.requires

.PHONY : CMakeFiles/cloud.dir/requires

CMakeFiles/cloud.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/cloud.dir/cmake_clean.cmake
.PHONY : CMakeFiles/cloud.dir/clean

CMakeFiles/cloud.dir/depend:
	cd "/home/jlurobot/Desktop/Camera calibration/View_Cloud/lidar2camera/View_Cloud/build" && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" "/home/jlurobot/Desktop/Camera calibration/View_Cloud/lidar2camera/View_Cloud" "/home/jlurobot/Desktop/Camera calibration/View_Cloud/lidar2camera/View_Cloud" "/home/jlurobot/Desktop/Camera calibration/View_Cloud/lidar2camera/View_Cloud/build" "/home/jlurobot/Desktop/Camera calibration/View_Cloud/lidar2camera/View_Cloud/build" "/home/jlurobot/Desktop/Camera calibration/View_Cloud/lidar2camera/View_Cloud/build/CMakeFiles/cloud.dir/DependInfo.cmake" --color=$(COLOR)
.PHONY : CMakeFiles/cloud.dir/depend

