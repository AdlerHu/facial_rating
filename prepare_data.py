import pandas as pd
import numpy as np
import os
import keras
from sklearn.model_selection import train_test_split
from utils.config import connect_db


# 從 DB 讀出之前用 DB 算出來的平均分數
def get_avg_ratings(connection):
    sql_str = f'''SELECT * FROM `avg_rating` WHERE 1 ;'''
    raw_data = pd.read_sql_query(sql_str, connection)
    return raw_data


# 將所有照片轉為 ndarray 格式
def image_to_ndarray():
    connection, cursor = connect_db()

    # filename avg_rating 的 dataframe
    labels_df = get_avg_ratings(connection)

    cursor.close()
    connection.close()

    # 資料集的照片大小固定是 350 * 350
    # 顏色信息通常由三個顏色通道組成，即紅色、綠色和藍色（RGB），每個通道的取值範圍為0-255。 channels就是指圖像的顏色通道數，對於RGB格式的圖像，通常是3。
    img_width, img_height, channels = 350, 350, 3
    # 資料集圖片目錄
    img_dir = '/home/adlerhu/facial_rating/dataset/SCUT-FBP5500_v2/Images/'
    # 資料集總共有 5500 張圖片
    nb_samples = len(os.listdir(img_dir))
    input_shape = (img_width, img_height, channels)

    img_total = np.empty((nb_samples, img_width, img_height, channels), dtype=np.float32)
    rating_total = np.empty((nb_samples, 1), dtype=np.float32)

    for i, filename in enumerate(os.listdir(img_dir)):
        # 讀取圖片
        img = keras.utils.load_img('%s%s' % (img_dir, filename))
        # 調用 keras.utils.img_to_array 函數將圖片轉換為 Numpy 數組，並將它們的形狀調整為指定的大小
        x = keras.utils.img_to_array(img).reshape(img_height, img_width, channels)
        # 將 ndarray 格式的 x 進行資料預處理，將其標準化 (Normalization) 到 [0, 1] 的範圍內
        x = x.astype('float32') / 255

        # 使用 Pandas 的 loc 方法，指定要查找的欄位名稱以及要查找的值
        y = labels_df.loc[labels_df['filename'] == filename, 'avg_rating'].values[0]
        y = y.astype('float32')

        img_total[i] = x
        rating_total[i] = y

    return img_total, rating_total


# 將數據拆分成訓練、驗證、測試集
def split_dataset():

    img_total, rating_total = image_to_ndarray()

    seed = 42
    # 將總集合分割為訓練集和測試集，其中 test_size 參數指定測試集的比例，這裡是 20%。random_state 參數設置隨機種子，以確保每次執行的結果都相同。
    img_train_all, img_test, rating_train_all, rating_test = train_test_split(img_total, rating_total, test_size=0.2, random_state=seed)
    # 將訓練集進一步分割為訓練集和驗證集，這樣就可以在訓練過程中使用驗證集來監控模型的性能，以避免過度擬合。
    img_train, img_val, rating_train, rating_val = train_test_split(img_train_all, rating_train_all, test_size=0.2, random_state=seed)

    np.save('dataset_npy/img_train.npy', img_train)
    np.save('dataset_npy/rating_train.npy', rating_train)
    np.save('dataset_npy/img_val.npy', img_val)
    np.save('dataset_npy/rating_val.npy', rating_val)
    np.save('dataset_npy/img_test.npy', img_test)
    np.save('dataset_npy/rating_test.npy', rating_test)

    # train: 3520, val: 880, test: 1100
    for item in [img_train, rating_train, img_val, rating_val, img_test, rating_test]:
        print(item.shape)
        

def main():
    split_dataset()


if __name__ == '__main__':
    main()
