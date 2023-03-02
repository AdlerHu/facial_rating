import MySQLdb
from utils.config import connect_db
from utils.predict import predict
from os import listdir
from os.path import join
import tensorflow as tf
import threading
from tensorflow.keras.models import load_model
import time


# 生成所有臉部照片列表
def create_face_table(cursor):
    smile = ['原始', '經典', '微笑', '合嘴', '不開心']
    hair_style = ['原始', '殺手', '短髮']
    beard = ['原始', '文青', '山羊鬍', '剃鬍', '小山羊鬍']
    glasses = ['原始', '寬邊', '寬邊矩形', '窄邊矩形', '寬邊橢圓', '窄邊橢圓']

    for i in smile:
        for j in hair_style:
            for k in beard:
                for l in glasses:
                    filename = f'{i}_{j}_{k}_{l}.jpg'
                    sql_str = f'INSERT INTO `my_face_rating` (`smile`, `hair_style`, `beard`, `glasses`, \
                                `filename`, `picture_done`, `rating`) \
                                VALUES (\"{i}\", \"{j}\", \"{k}\", \"{l}\", \
                                \"{filename}\" , "0", 0.0);'

                    try:
                        cursor.execute(sql_str)
                    except Exception as err:
                        print(err.args)


# 將一個list按餘數切分成多個子list
def split_list_by_mod(lst, mod):
    return [lst[i::mod] for i in range(mod)]


# 讀取製作好的所有圖片，並按線程數切成幾個list
def prepare_face_lists(myface_dir, threading_number):
    return split_list_by_mod(listdir(myface_dir), threading_number)


def evaluate_faces(myface_dir, face_list, model):
    db, cursor = connect_db()
    for filename in face_list:
        fullpath = join(myface_dir, filename)
        result, points = predict(img_path=fullpath, model=model)
        update_my_face_rating(cursor, points=points, filename=filename)
    cursor.close()
    db.close()


# 將模型預測的結果寫入DB
def update_my_face_rating(cursor, points, filename):
    sql_str = f'UPDATE `my_face_rating` SET `rating` = {points}, `picture_done` = "1" WHERE `filename` = \"{filename}\";'
    try:
        cursor.execute(sql_str)
    except Exception as err:
        print(err.args)
    

def main(myface_dir, threading_number):

    model = load_model('model/21-0.12.h5')

    # 第一次執行程式要create table 
    db, cursor = connect_db()
    create_face_table(cursor)

    face_lists = prepare_face_lists(myface_dir, threading_number)

    # 創建多線程寫入數據
    threads = []
    for i in range(threading_number):
        t = threading.Thread(target=evaluate_faces, args=(myface_dir, face_lists[i], model))
        threads.append(t)
    
    # 啟動線程
    for t in threads:
        t.start()

    # 等待線程完成
    for t in threads:
        t.join()

    cursor.close()
    db.close()
    print('Done')


if __name__ == '__main__':
    start = time.time()
    myface_dir = '/home/adlerhu/Documents/GitHub/facial_rating/my_face/'

    # threading_number: 預計跑的線程數
    main(myface_dir, threading_number=8)
    end = time.time()
    print(f'It take\'s {end-start} seconds to run.')
