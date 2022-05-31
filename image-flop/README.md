# Image-flop
A simple image processing program built in QML.

## Requirements
CMake
VS2015
opencv 3.1.0
Qt 5.7

## Building on Windows
The instructions are rough due to loss of memory regarding the procedure. Beware, there might be obstacles ahead!

- Install Visual Studio 2015.
- Download opencv 3.1.0, place it in a folder called ext and build it using VS2015.
  Easiest way is to download CMake-Gui and select the CMakeLists.txt that they've provided.
  Once the build is configured in cmake, open to generated VS2015 solution and build the install
  configuration for both Release/Debug.
- Download and install Qt 5.7 in the ext folder as well.
- Use CMake-Gui to build image-flop by directing it to the ext folder and the approriate Qt folder.
  Modifications to the CMakeLists.txt in process-eye might be necessary to match your opencv path.

## Building on Linux
- Use CMake-Gui and select image-flop as source folder and set whichever build folder you'd like.
- Press Configure and create a folder called ext, select that as your ext folder.
- If you're on a 64-bit computer, download Qt 5.7 with the online installer.
  For 32-bit users, you need to build Qt 5.7 by yourself since there's no build available.
- Once installed, set Qt5-DIR as the folder <qt folder>/5.7/gcc/lib/cmake/Qt5.
  If you're unsure, the folder should contain Qt5Config.cmake.
- Download the correct version of OpenCV (3.1 for either 32-bit or 64-bit) and place it in your ext folder.

### Building Qt
- Download the open source code from qt.io and follow instructions.
- QtQuick requires OpenGL to build, so run "sudo apt-get install mesa-common-dev libgl1-mesa-dev libglu1-mesa-dev".
- I had to install the package "libxcb-xinerama0-dev" for some reason.
- Run this in the Qt folder: ./configure -prefix $PWD/qtbase -opensource -nomake tests -nomake examples -opengl
- Results end up in the qtbase folder.

### Building OpenCV
- Use CMake-Gui to set the opencv folder as source and set your desired build folder.
- Go to http://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html and install the things you deem necessary.
- I removed some unnecessary options in the build configuration (MATLAB, CUDA, et.c.) then used Make Unix files, such that once CMake has generated the make files.
- Make sure you set the flag CMAKE_INSTALL_PREFIX to the install folder you want and run "make install" in the build folder.
- Copy the install folder to ext and rename it to opencv.

