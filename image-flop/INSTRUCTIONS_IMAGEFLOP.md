# Image-flop
A simple image processing program built in QML.

## Requirements
CMake
VS2015
opencv 3.1.0
Qt 5.7

## Building
The instructions are rough due to loss of memory regarding the procedure. Beware, there might be obstacles ahead!

- Install Visual Studio 2015.
- Download opencv 3.1.0, place it in a folder called ext and build it using VS2015.
  Easiest way is to download CMake-Gui and select the CMakeLists.txt that they've provided.
  Once the build is configured in cmake, open to generated VS2015 solution and build the install configuration
  for both Release/Debug.
- Download and install Qt 5.7 in the ext folder as well.
- Use CMake-Gui to build process-eye by directing it to the ext folder and the approriate Qt folder.
  Modifications to the CMakeLists.txt in process-eye might be necessary to match your opencv path.