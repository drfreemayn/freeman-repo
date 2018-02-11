# Convolutional Neural Networks
This is a guide on how to train neural networks on GPU in Python with the Keras framework using Theano as backend.

## Instructions
- Download and install NVIDIA CUDA Toolkit (cuDNN 5.1 is optinal)
- Download and install Anaconda 3. We need it since we don't want to build LAPACK/BLAS.
- Make sure there are no other python paths in PATH
- Create a virtual environment for all necessary python packages
<p>`conda create -n kerasenv python=3.6.1`
<p>`conda install scipy`
<p>`pip install keras matplotlib Pillow h5py`

## Test your environment
Activate the virtual environment:
`source activate kerasenv`

Run MNIST test program:
`python mnist_test.py --weights test.h5py --train --test`

## Cifar10 Challenge
Run the previously trained network:
`python cifar10_challenge.py --test`

To train and test a new network:
`python cifar10_challenge.py --weights test.h5py --train --test`