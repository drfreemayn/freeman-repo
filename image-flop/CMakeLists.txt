cmake_minimum_required (VERSION 2.6)
project (image-flop)

set(CMAKE_CONFIGURATION_TYPES "Debug;Release" CACHE STRING "" FORCE)

if(NOT CMAKE_BUILD_TYPE)
   set(CMAKE_BUILD_TYPE "Release" CACHE STRING
       "Choose the type of build, options are: Debug Release"
       FORCE)
endif(NOT CMAKE_BUILD_TYPE)

if(NOT EXT)
   set(EXT "" CACHE PATH
       "Define where EXT is located."
       FORCE)
   message(FATAL_ERROR "Define EXT directory." )
endif()

SET(CMAKE_INSTALL_PREFIX "install")

SET(OpenCV_INCLUDE_DIRS "${EXT}/opencv3.1/opencv/install/include")
include_directories("${OpenCV_INCLUDE_DIRS}")

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

include_directories("${CMAKE_SOURCE_DIR}/include")

SET(SRC_FILES src/main.cpp
              src/imageprocessor.cpp
              src/mat_and_qimage.cpp)

SET(HEADER_FILES include/imageprocessor.h
                 include/mat_and_qimage.hpp)

set(CMAKE_AUTOMOC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

find_package(Qt5 COMPONENTS Quick Core Qml Gui)
qt5_add_resources(RESOURCES resources.qrc)
add_executable(image-flop ${SRC_FILES} ${HEADER_FILES} ${RESOURCES})
qt5_use_modules(image-flop Quick Core Qml Gui)

target_link_libraries (image-flop ${OPENCV_LIBS})