# Convolutional Neural Networks
This is a guide on how to train neural networks on GPU in Python with the Keras framework.

## Instructions
- Download and install [Python3](https://www.python.org/downloads/).
- Install virtualenv: `pip install virtualenv`.
- Create a virtual environment: `virtualenv venv`
- Activate the environment: `venv\Scripts\activate`
- If you have issues with execution policies: `Set-ExecutionPolicy Unrestricted -Scope Process`
- Install requirements: `pip install -r requirements.txt`

## Test your environment

Run MNIST test program:
`python mnist_test.py --weights test.h5 --train --test`

## Cifar10 Challenge
Run the previously trained network:
`python cifar10_challenge.py --test`

To train and test a new network:
`python cifar10_challenge.py --weights test.h5 --train --test`