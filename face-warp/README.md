# Face Warp
A program for warping faces together with piece-wise affine transformations.

## Requirements

- Download and install [Python3](https://www.python.org/downloads/).
- Download and install [Visual Studio with C++ compiler](https://visualstudio.microsoft.com/vs/features/cplusplus/).
- Download a [facial landmark shape predictor](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) and place in the `face-warp` folder.
- Install virtualenv: `pip install virtualenv`.
- Create a virtual environment: `virtualenv venv`
- Activate the environment: `venv\Scripts\activate`
- If you have issues with execution policies: `Set-ExecutionPolicy Unrestricted -Scope Process`
- Install requirements: `pip install -r requirements.txt`

## Usage 

To execute using default images:

`python face-warp.py`