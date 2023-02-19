import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.applications.resnet50 import ResNet50
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau


# 取出先前切好的各訓練集
def get_dataset():
    x_train = np.load('../dataset_npy/x_train.npy')
    y_train = np.load('../dataset_npy/y_train.npy')
    x_val = np.load('../dataset_npy/x_val.npy')
    y_val = np.load('../dataset_npy/y_val.npy')
    x_test = np.load('../dataset_npy/x_test.npy')
    y_test = np.load('../dataset_npy/y_test.npy')

    # for shit in [x_train, y_train, x_val, y_val, x_test, y_test]:
    #     print(shit.shape)

    return x_train, y_train, x_val, y_val, x_test, y_test


# 
def train_model():

    img_width, img_height, channels = 350, 350, 3
    input_shape = (img_width, img_height, channels)
    x_train, y_train, x_val, y_val, x_test, y_test = get_dataset()

    resnet = ResNet50(include_top=False, pooling='avg', input_shape=input_shape)
    model = Sequential()
    model.add(resnet)
    model.add(Dense(1))
    model.layers[0].trainable = False
    # print(model.summary())

    filepath = '../model/{epoch:02d}-{val_loss:.2f}.h5'
    checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
    reduce_learning_rate = ReduceLROnPlateau(monitor='loss', factor=0.1, patience=2, cooldown=2, min_lr=0.00001, verbose=1)
    callback_list = [checkpoint, reduce_learning_rate]

    model.layers[0].trainable = True
    model.compile(loss='mse', optimizer='adam')
    history = model.fit(x=x_train,y=y_train, batch_size=8, epochs=40, validation_data=(x_val, y_val), callbacks=callback_list)

    # plt.scatter(y_test, model.predict(x_test))
    # plt.plot(y_test, y_test, 'ro')
    # plt.show()


def main():
    train_model()


if __name__ == '__main__':
    main()