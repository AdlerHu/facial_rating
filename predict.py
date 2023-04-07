from PIL import Image
from keras.utils import img_to_array


def predict(model, img_path):

    # 使用 pillow 讀取圖片
    img = Image.open(img_path)

    # 傳入的圖片要縮放到跟資料集圖片一樣的大小
    img_width, img_height, channels = 350, 350, 3
    img = img.resize([img_width, img_height])

    # 將縮放過的圖片轉換成 ndarray 
    test_img = img_to_array(img).reshape(img_height, img_width, channels)
    test_img = test_img / 255
    test_img = test_img.reshape((1,) + test_img.shape)

    prediction = model.predict(test_img)

    # 滿分5分，得分超過 3 就認定為好看
    points = round(float(prediction[0][0]), 3)
    result = '好看' if points > 3 else '普通'
    return result, points
