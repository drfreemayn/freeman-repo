import math
import numpy as np
import argparse as ap

import keras.backend as K
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import InputLayer, Dense, Activation, Flatten, Dropout
from keras.layers.normalization import BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint, LearningRateScheduler
from keras.datasets import cifar10
from keras.utils import np_utils

import matplotlib.pyplot as plt

np.random.seed(1337)

NUM_EPOCS = 100
BATCH_SIZE = 32
VERBOSE = 1
PATIENCE = 10

NUM_CLASSES = 10

def preprocess_input(x):
    x = x.astype('float32')
    x /= 255.
    x -= 0.5
    x *= 2.
    return x

def load_data():
    # Define inputs image dimensions
    img_rows, img_cols, num_channels = 32, 32, 3

     # Load data
    (X_train, y_train), (X_test, y_test) = cifar10.load_data()

    if K.image_data_format() == 'channels_first':
        X_train = X_train.reshape(X_train.shape[0], num_channels, img_rows, img_cols)
        X_test = X_test.reshape(X_test.shape[0], num_channels, img_rows, img_cols)
        input_shape = (num_channels, img_rows, img_cols)
    else:
        X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, num_channels)
        X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, num_channels)
        input_shape = (img_rows, img_cols, num_channels)

    X_train = preprocess_input(X_train)
    X_test = preprocess_input(X_test)

    # Convert 1-dimensional class arrays to 10-dimensional class matrices
    Y_train = np_utils.to_categorical(y_train, NUM_CLASSES)
    Y_test = np_utils.to_categorical(y_test, NUM_CLASSES)

    # Define dicts
    train_data = {}
    train_data['X'] = X_train
    train_data['Y'] = Y_train

    test_data = {}
    test_data['X'] = X_test
    test_data['Y'] = Y_test

    return train_data, test_data, input_shape

def conv2d_bn(model, num_filters, filter_size):
    if K.image_data_format() == 'channels_first':
        bn_axis = 1
    else:
        bn_axis = -1

    model.add(Convolution2D(num_filters, filter_size, padding='same', use_bias=False))
    model.add(BatchNormalization(axis=bn_axis))
    model.add(Activation('relu'))
    return model

def create_model(input_shape):

    # Define network architecture and compile
    model = Sequential()
    model.add(InputLayer(input_shape=input_shape))

    # Block 1
    model = conv2d_bn(model, 64, (3,3))
    model = conv2d_bn(model, 64, (3,3))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Dropout(0.25))

    # Block 2
    model = conv2d_bn(model, 128, (3,3))
    model = conv2d_bn(model, 128, (3,3))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Dropout(0.25))

    # Block 3
    model = conv2d_bn(model, 128, (3,3))
    model = conv2d_bn(model, 128, (3,3))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Dropout(0.25))

    # Classification block
    model.add(Flatten())
    model.add(Dense(500))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.25))
    model.add(Dense(NUM_CLASSES, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model

def step_decay(epoch):
    # learning rate schedule
    initial_lrate = 0.001
    drop = 0.1
    epochs_drop = 10.0
    lrate = initial_lrate * math.pow(drop, math.floor((1+epoch)/epochs_drop))
    return np.max([lrate, 0.00001])

def train(train_data, val_data, model, weights_path):
    # Define callbacks
    earlystop = EarlyStopping(monitor='val_acc',
                              patience=PATIENCE,
                              verbose=VERBOSE)
    checkpoint = ModelCheckpoint(weights_path,
                                 monitor='val_acc',
                                 verbose=VERBOSE,
                                 save_best_only=True,
                                 save_weights_only=True)
    lrate = LearningRateScheduler(step_decay)

    # Compile and train
    model.fit(train_data['X'], train_data['Y'],
              batch_size=BATCH_SIZE,
              epochs=NUM_EPOCS,
              validation_data=(val_data['X'], val_data['Y']),
              callbacks=[earlystop, checkpoint, lrate],
              verbose=VERBOSE)

def test(data, model, weights_path):
    # Load weights and evaluate
    model.load_weights(weights_path)
    score = model.evaluate(data['X'], data['Y'],
                           verbose=VERBOSE)
    print('\nTest loss:', score[0])
    print('\nTest accuracy:', score[1])

def parse_args():
    parser = ap.ArgumentParser()
    parser.add_argument("--weights", help="Path to network weights.",
                        default="cifar10_weights.h5py")
    parser.add_argument("--train", help="Train a new network.",
                        action="store_true")
    parser.add_argument("--test", help="Test the current network.",
                        action="store_true")
    return parser.parse_args()

def main():
    args = parse_args()

    train_data, test_data, input_shape = load_data()
    model = create_model(input_shape)

    if not (args.train or args.test):
        print('\nYou succesfully ran the script with no action. Add --test or --train!')

    if args.train:
        train(train_data, test_data, model, args.weights)

    if args.test:
        test(test_data, model, args.weights)

if __name__ == '__main__':
    main()
