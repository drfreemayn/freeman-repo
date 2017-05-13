# Convolutional Neural Networks
This is a guide on how to train neural networks on GPU in Python with the Keras framework using Theano as backend.

## Instructions
- Download and install NVIDIA CUDA Toolkit (cuDNN 5.1 is optinal)
- Download and install Anaconda 3. We need it since we don't want to build LAPACK/BLAS.
- Make sure there are no other python paths in PATH
- Create a virtual environment for all necessary python packages
conda create -n kerasenv python=3.6.1
- conda install scipy
- pip install keras matplotlib Pillow h5py

## Test your environment
- activate kerasenv
- python mnist_test.py --weights test.h5py --train --test