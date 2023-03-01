from tensorflow import keras
from random import randint
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# 用測試集資料驗證模型成果
# def predict():
#     model = keras.models.load_model('03-0.27.h5')

#     plt.rcParams['font.size'] = 9
#     plt.rcParams['figure.figsize'] = (9, 9)
    
#     x_test = np.load('x_test.npy')
#     y_test = np.load('y_test.npy')

#     nb_test_samples = x_test.shape[0]
#     nb_rows, nb_cols = 5, 5

#     for k in range(nb_rows * nb_cols):
#         i = randint(0, nb_test_samples -1)
#         prediction = model.predict(x_test[i].reshape((1, ) + x_test[i].shape))
#         plt.subplot(nb_rows, nb_cols, k+1)
#         plt.imshow(x_test[i])
#         plt.title('p:%.2f a:%.2f' % (prediction[0][0], y_test[i]))
#         plt.axis('off')

#     plt.show()


# 
def predict(img_path):
    model = keras.models.load_model('model/21-0.12.h5')

    plt.rcParams['font.size'] = 9
    plt.rcParams['figure.figsize'] = (9, 9)    

    img = Image.open(img_path)
    plt.imshow(img)
    img_width, img_height, channels = 350, 350, 3
    img = img.resize([img_width, img_height])
    
    test_x = keras.utils.img_to_array(img).reshape(img_height, img_width, channels)
    test_x = test_x / 255
    test_x = test_x.reshape((1,) + test_x.shape)

    # prediction = model.predict(test_x)
    prediction = model(test_x, training=False)

    points = round(float(prediction[0][0]), 3)
    result = '美' if points > 3 else '醜'


    #  參考文檔將預測結果分成5等第呈現
    # lv, p = 0, 0
    # if (prediction[0][0] <= 1):
    #     lv = 1
    #     p = 20
    # elif (prediction[0][0] > 1) and (prediction[0][0] <= 2):
    #     lv = 2
    #     p = 40
    # elif (prediction[0][0] > 2) and (prediction[0][0] <= 3):
    #     lv = 3
    #     p = 60
    # elif (prediction[0][0] > 3) and (prediction[0][0] <= 4):
    #     lv = 4
    #     p = 80
    # elif (prediction[0][0] > 4) and (prediction[0][0] <= 5):
    #     lv = 5
    #     p = 100
    # print(f'prediction: {lv}, 贏過{p}%的人')

    return result, points


def predict2(img_path, model):
    
    plt.rcParams['font.size'] = 9
    plt.rcParams['figure.figsize'] = (9, 9)    

    img = Image.open(img_path)
    img_width, img_height, channels = 350, 350, 3
    img = img.resize([img_width, img_height])
    
    test_x = keras.utils.img_to_array(img).reshape(img_height, img_width, channels)
    test_x = test_x / 255
    test_x = test_x.reshape((1,) + test_x.shape)
    prediction = model.predict(test_x)

    points = round(float(prediction[0][0]), 3)
    
    return points
