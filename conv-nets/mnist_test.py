import numpy as np
import argparse as ap

import keras.backend as K
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Dense, Flatten, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import load_model

np.random.seed(1337)

NUM_EPOCS = 100
BATCH_SIZE = 32
VERBOSE = 1
PATIENCE = 5

NUM_CLASSES = 10

def load_data():
    # Define inputs image dimensions
    img_rows, img_cols = 28, 28

     # Load data
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    
    if K.image_data_format() == 'channels_first':
        X_train = X_train.reshape(X_train.shape[0], 1, img_rows, img_cols)
        X_test = x_test.reshape(X_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 1)
        X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)
    
    # Convert type and scale
    X_train = X_train.astype('float32') / 255
    X_test = X_test.astype('float32') / 255  

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

def create_model(input_shape):
    # Define network architecture and compile
    model = Sequential()
    model.add(Convolution2D(16, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(4, 4)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(NUM_CLASSES, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model

def train(train_data, val_data, model, weights_path):
    # Define callbacks
    earlystop = EarlyStopping(monitor='val_accuracy',
                              patience=PATIENCE, 
                              verbose=VERBOSE)
    checkpoint = ModelCheckpoint(weights_path,
                                 monitor='val_accuracy',
                                 verbose=VERBOSE,
                                 save_best_only=True,
                                 save_weights_only=False)
    
    # Compile and train
    model.fit(train_data['X'], train_data['Y'],
              batch_size=BATCH_SIZE,
              epochs=NUM_EPOCS,
              validation_data=(val_data['X'], val_data['Y']),
              callbacks=[earlystop, checkpoint],
              verbose=VERBOSE)

def test(data, model, weights_path):
    # Load weights and evaluate
    model = load_model(weights_path)
    score = model.evaluate(data['X'], data['Y'],
                           verbose=VERBOSE)
    print('\nTest loss:', score[0])
    print('\nTest accuracy:', score[1])

def parse_args():
    parser = ap.ArgumentParser()
    parser.add_argument("--weights", help="Path to network weights.",
                        default="mnist_weights.h5py")
    parser.add_argument("--train", help="Train a new network.",
                        action="store_true")
    parser.add_argument("--test", help="Test the current network.",
                        action="store_true")
    return parser.parse_args()

def main():
    args = parse_args()

    train_data, test_data, input_shape = load_data()
    model = create_model(input_shape)

    if args.train:
        train(train_data, test_data, model, args.weights)
    
    if args.test:
        test(test_data, model, args.weights)

if __name__ == '__main__':
    main()