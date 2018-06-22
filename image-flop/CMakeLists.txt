cmake_minimum_required (VERSION 2.6)
project (image-flop)

set(CMAKE_CONFIGURATION_TYPES "Debug;Release" CACHE STRING "" FORCE)

if(NOT CMAKE_BUILD_TYPE)
   set(CMAKE_BUILD_TYPE "Release" CACHE STRING
       "Choose the type of build, options are: Debug Release"
       FORCE)
endif(NOT CMAKE_BUILD_TYPE)

IF(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  SET(CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_BINARY_DIR }/install" CACHE PATH
      "Set the desired install path"
      FORCE)
ENDIF(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)

if(NOT EXT)
   set(EXT "" CACHE PATH
       "Define where EXT is located."
       FORCE)
   message(FATAL_ERROR "Define EXT directory." )
endif()

if(MSVC) # Check if we are using the Visual Studio compiler
    SET(LIB_PREFIX "")
    SET(LIB_SUFFIX ".lib")
    SET(OPENCV_VER "310")

    SET(OpenCV_INCLUDE_DIRS "${EXT}/opencv3.1/opencv/install/include")
    SET(OpenCV_LIB_DIR "${EXT}/opencv3.1/opencv/install/x64/vc14/lib")
else()
    SET(LIB_PREFIX "lib")
    SET(LIB_SUFFIX ".so")
    SET(OPENCV_VER"")

    SET(OpenCV_INCLUDE_DIRS "${EXT}/opencv/include")
    SET(OpenCV_LIB_DIR "${EXT}/opencv/lib")
endif()

include_directories("${OpenCV_INCLUDE_DIRS}")
link_directories("${OpenCV_LIB_DIR}")

if (CMAKE_BUILD_TYPE MATCHES "Release")
  SET(OPENCV_LIBS "${LIB_PREFIX}opencv_core${OPENCV_VER}${LIB_SUFFIX}"
                  "${LIB_PREFIX}opencv_imgproc${OPENCV_VER}${LIB_SUFFIX}")
elseif (CMAKE_BUILD_TYPE MATCHES "Debug")
  SET(OPENCV_LIBS "${LIB_PREFIX}opencv_core${OPENCV_VER}d${LIB_SUFFIX}"
                  "${LIB_PREFIX}opencv_imgproc${OPENCV_VER}d${LIB_SUFFIX}")
endif ()

include_directories("${CMAKE_SOURCE_DIR}/include")

SET(SRC_FILES src/main.cpp
              src/imageprocessor.cpp
              src/mat_and_qimage.cpp)

SET(HEADER_FILES include/imageprocessor.h
                 include/mat_and_qimage.hpp)

FILE(GLOB QML_SRC "qml/*.qml")

set(CMAKE_AUTOMOC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

find_package(Qt5 COMPONENTS Quick Core Qml Gui)
qt5_add_resources(RESOURCES resources.qrc)
add_executable(image-flop ${SRC_FILES} ${HEADER_FILES} ${RESOURCES} ${QML_SRC})
qt5_use_modules(image-flop Quick Core Qml Gui)

target_link_libraries (image-flop ${OPENCV_LIBS})
