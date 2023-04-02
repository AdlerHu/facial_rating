import numpy as np
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.applications.resnet50 import ResNet50
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras.models import load_model


# 取出先前切好的各訓練集
def get_dataset():
    img_train = np.load('dataset_npy/img_train.npy')
    rating_train = np.load('dataset_npy/rating_train.npy')
    img_val = np.load('dataset_npy/img_val.npy')
    rating_val = np.load('dataset_npy/rating_val.npy')
    img_test = np.load('dataset_npy/img_test.npy')
    rating_test = np.load('dataset_npy/rating_test.npy')
    return img_train, rating_train, img_val, rating_val, img_test, rating_test


def train_model():
    img_train, rating_train, img_val, rating_val, img_test, rating_test = get_dataset()

    # 使用 Keras 內建的 ResNet50 架構進行訓練，去掉最後的 softmax 層，然後再加上一層 dense 全連接層，
    # 並將 ResNet50 模型的其餘參數設為不可訓練，使其先直接訓練最後的 dense 層參數。
    resnet = ResNet50(include_top=False, pooling='avg', input_shape=(350, 350, 3))
    model = Sequential()
    model.add(resnet)
    model.add(Dense(1))
    model.layers[0].trainable = False

    # 使用了Keras中的回調函數，用於在訓練過程中監控和調整模型的性能和學習率。具體來說定義兩個回調函數：
    # ModelCheckpoint：在每個epoch結束時保存模型的權重到指定的文件路徑，以及在驗證集上監控損失函數，並保存最佳模型的權重。
    # ReduceLROnPlateau：在損失函數不再下降時降低學習率，以便更好地優化模型參數。

    filepath = 'model/{epoch:02d}-{val_loss:.2f}.h5'
    checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
    reduce_learning_rate = ReduceLROnPlateau(monitor='loss', factor=0.1, patience=2, cooldown=2, min_lr=0.00001, verbose=1)
    callback_list = [checkpoint, reduce_learning_rate]

    # 接下來，模型的第一層被設置為可訓練，並使用mse作為損失函數，adam作為優化器來訓練模型。
    # 模型在訓練過程中，將輸入圖像數據x和目標評分數據y傳入模型進行訓練，並設置batch_size=8，epochs=30。
    # 在每個epoch結束時，使用驗證集的數據進行模型評估，並通過定義的回調函數進行模型性能監控和調整。
    model.layers[0].trainable = True
    model.compile(loss='mse', optimizer='adam')
    history = model.fit(x=img_train,y=rating_train, batch_size=8, epochs=30, validation_data=(img_val, rating_val), callbacks=callback_list)


def main():
    train_model()


if __name__ == '__main__':
    main()