import keras
import matplotlib.pyplot as plt
from PIL import Image

 
def predict(img_path):
    model = keras.models.load_model('model/26-0.12.h5')

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
    return result, points
