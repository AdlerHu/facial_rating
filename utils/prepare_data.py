import MySQLdb
import pandas as pd
import numpy as np
from collections import Counter
import os
import keras
from sklearn.model_selection import train_test_split
from config import connect_db


# 從 DB 讀出之前用 DB 算出來的平均分數
def get_avg_ratings(db):
    sql_str = f'''SELECT * FROM `avg_rating` WHERE 1 ;'''
    raw_data = pd.read_sql_query(sql_str, db)
    return raw_data


# 得到每張照片的平均分數
# 參考文件用程式算平均分數，很慢，棄用
# def get_avg_ratings():
#     ratings = pd.read_excel('/home/adlerhu/pycode/facial_rating/SCUT-FBP5500_v2.1/SCUT-FBP5500_v2/All_Ratings.xlsx')
#     filenames = ratings.groupby('Filename').size().index.tolist()

#     labels = []

#     for filename in filenames:
#         df = ratings[ratings['Filename'] == filename]
#         count = Counter(df['Rating']).most_common(1)[0][0]
#         score = round(df['Rating'].mean(), 2)
#         labels.append({'Filename': filename, 'most_common': count, 'score': score})

#     # 每張照片的平均分數 
#     labels_df = pd.DataFrame(labels)
    
#     return labels_df


# 將所有照片轉為 ndarray 格式
def image_to_ndarray():
    db, cursor = connect_db()
    labels_df = get_avg_ratings(db=db)

    cursor.close()
    db.close()

    img_width, img_height, channels = 350, 350, 3
    smaple_dir = '/home/adlerhu/pycode/facial_rating/SCUT-FBP5500_v2.1/SCUT-FBP5500_v2/Images/'
    nb_samples = len(os.listdir(smaple_dir))
    input_shape = (img_width, img_height, channels)

    x_total = np.empty((nb_samples, img_width, img_height, channels), dtype=np.float32)
    y_total = np.empty((nb_samples, 1), dtype=np.float32)

    for i, fn in enumerate(os.listdir(smaple_dir)):
        img = keras.utils.load_img('%s%s' % (smaple_dir, fn))
        x = keras.utils.img_to_array(img).reshape(img_height, img_width, channels)
        x = x.astype('float32') / 255
        y = labels_df[labels_df.filename == fn].avg_rating.values
        y = y.astype('float32')

        x_total[i] = x
        y_total[i] = y

    return x_total, y_total


# 將數據拆分成訓練、驗證、測試集
def split_dataset():

    x_total, y_total = image_to_ndarray()

    seed = 42
    x_train_all, x_test, y_train_all, y_test = train_test_split(x_total, y_total, test_size=0.2, random_state=seed)
    x_train, x_val, y_train, y_val = train_test_split(x_train_all, y_train_all, test_size=0.2, random_state=seed)

    # train: 3520, val: 880, test: 1100  
    np.save('../dataset_npy/x_train.npy', x_train)
    np.save('../dataset_npy/y_train.npy', y_train)
    np.save('../dataset_npy/x_val.npy', x_val)
    np.save('../dataset_npy/y_val.npy', y_val)
    np.save('../dataset_npy/x_test.npy', x_test)
    np.save('../dataset_npy/y_test.npy', y_test)
    
    # for item in [x_train, y_train, x_val, y_val, x_test, y_test]:
    #     print(item.shape)
        

def main():
    split_dataset()


if __name__ == '__main__':
    main()