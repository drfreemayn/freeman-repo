cmake_minimum_required (VERSION 2.6)
set(CMAKE_CONFIGURATION_TYPES Debug Release)
project (process-eye)

if(NOT CMAKE_BUILD_TYPE)
   set(CMAKE_BUILD_TYPE "Release" CACHE STRING
       "Choose the type of build, options are: Debug Release"
       FORCE)
endif(NOT CMAKE_BUILD_TYPE)

if(NOT EXT)
   set(EXT "" CACHE PATH
       "Define where EXT is located."
       FORCE)
endif()

SET(OpenCV_INCLUDE_DIRS "${EXT}/opencv3.1/opencv/install/include")
INCLUDE_DIRECTORIES("${OpenCV_INCLUDE_DIRS}")
         
SET(OpenCV_LIB_DIR "${EXT}/opencv3.1/opencv/install/x64/vc14/lib")
link_directories("${OpenCV_LIB_DIR}")

if (CMAKE_BUILD_TYPE MATCHES "Release")
  SET (OPENCV_LIBS opencv_calib3d310.lib
                   opencv_core310.lib
                   opencv_features2d310.lib
                   opencv_flann310.lib
                   opencv_highgui310.lib
                   opencv_imgcodecs310.lib
                   opencv_imgproc310.lib
                   opencv_ml310.lib
                   opencv_objdetect310.lib
                   opencv_photo310.lib
                   opencv_shape310.lib
                   opencv_stitching310.lib
                   opencv_superres310.lib
                   opencv_ts310.lib
                   opencv_video310.lib
                   opencv_videoio310.lib
                   opencv_videostab310.lib)
elseif (CMAKE_BUILD_TYPE MATCHES "Debug")
  SET (OPENCV_LIBS opencv_calib3d310d.lib
                   opencv_core310d.lib
                   opencv_features2d310d.lib
                   opencv_flann310d.lib
                   opencv_highgui310d.lib
                   opencv_imgcodecs310d.lib
                   opencv_imgproc310d.lib
                   opencv_ml310d.lib
                   opencv_objdetect310d.lib
                   opencv_photo310d.lib
                   opencv_shape310d.lib
                   opencv_stitching310d.lib
                   opencv_superres310d.lib
                   opencv_ts310d.lib
                   opencv_video310d.lib
                   opencv_videoio310d.lib
                   opencv_videostab310d.lib)
endif ()

add_executable(process-eye process-eye.cpp)

target_link_libraries (process-eye "${OPENCV_LIBS}")