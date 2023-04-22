import matplotlib
import keras
from random import randint
import matplotlib.pyplot as plt
import numpy as np


# 用測試集資料驗證模型成果
def verify():
    model = keras.models.load_model('model/26-0.12.h5')

    plt.rcParams['font.size'] = 9
    plt.rcParams['figure.figsize'] = (10, 10)
    
    img_test = np.load('dataset_npy/img_test.npy')
    rating_test = np.load('dataset_npy/rating_test.npy')

    nb_test_samples = img_test.shape[0]
    nb_rows, nb_cols = 5, 5

    for k in range(nb_rows * nb_cols):
        i = randint(0, nb_test_samples -1)
        prediction = model.predict(img_test[i].reshape((1, ) + img_test[i].shape))
        plt.subplot(nb_rows, nb_cols, k+1)
        plt.imshow(img_test[i])
        plt.title('pred:%.2f real:%.2f' % (prediction[0][0], rating_test[i]))
        plt.axis('off')

    plt.show()

verify()