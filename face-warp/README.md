# Face Warp
A program for warping faces together with piece-wise affine transformations.

## Requirements
Python 2.7.x (64-bit)
CMake
dlib (https://github.com/davisking/dlib)
boost.python (http://www.boost.org/)
opencv (http://opencv.org/downloads.html)
numpy

To get dlib, use git clone in bash. For boost, download the latest version of the source files (my version was 1.59.0).
For opencv, download the latest version of the source files (my version was 3.1.0).

## Usage 
Place the file opencv2.pyd in C:\Python27\Lib\site-packages, I found it in opencv3.1\opencv\build\python\2.7\x64.
If problem arises, you might need to add the site-packages folder to your PATH.

Download a facial landmark shape predictor from http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2 and place in the script folder.

To use dlib the library boost.python has to be built unfortunately.
This was my procedure for MSVC 2015:

- In the boost source folder, run bootstrap.bat in cmd.
- Run "b2 install", make sure that CMake selects MSCV 2015 as default compiler. Otherwise add toolset=mscv afterwards.
- When the building is finished, find the lib directory and see that there's files called that begins with "libboost_python-vc140".
- Make a system variable called BOOST_LIBRARYDIR and add that folder.
- Make another system variable called BOOST_ROOT and add the include directory "C:\Boost\include\boost-1_59" or the boost source directory.
- In the dlib directory, run python setup.py install. Hopefully dlib now finds the boost.python library. Otherwise follow the instructions.
- To see that dlib has been installed correctly, run pip freeze and there should be a dlib package available.