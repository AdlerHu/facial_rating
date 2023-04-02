import MySQLdb
from utils.config import connect_db
from utils.predict import predict
from os import listdir
from os.path import join
import tensorflow as tf


# 生成所有臉部照片的資料表
def prepare_face_pics(cursor):
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
                                `filename`, `rating`) \
                                VALUES (\"{i}\", \"{j}\", \"{k}\", \"{l}\", \
                                \"{filename}\", 0.0);'

                    try:
                        cursor.execute(sql_str)
                    except Except as err:
                        print(err.args)


# 讀取製作好的所有圖片
def evaluate_all_faces(cursor):
    face_path = '/home/adlerhu/facial_rating/my_face/'
    files = listdir(face_path)
    for f in files:
        fullpath = join(face_path, f)
        result, points = predict(img_path=fullpath)
        # print(f'result: {result}, points: {points}')
        update_my_face_rating(cursor, points=points, filename=f)


# 將模型預測的結果寫入DB
def update_my_face_rating(cursor, points, filename):
    sql_str = f'UPDATE `my_face_rating` SET `rating` = {points} WHERE `filename` = \"{filename}\";'
    try:
        cursor.execute(sql_str)
    except Except as err:
        print(err.args)


def main():

    db, cursor = connect_db()    
    prepare_face_pics(cursor)
    evaluate_all_faces(cursor)

    cursor.close()
    db.close()
    print('done')


if __name__ == '__main__':
    main()