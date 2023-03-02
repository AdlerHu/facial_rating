from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
from datetime import timedelta
from utils.predict import predict
from tensorflow.keras.models import load_model
 

# 設定允許的圖片格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)

# 緩存過期時間
app.send_file_max_age_default = timedelta(seconds=5)


# 啟動webapp時就先載好模型，而不是有需要預測時再載入，提升效率
@app.before_first_request
def prepare_model():
    global model 
    model = load_model('model/21-0.12.h5')


# route 
@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)): 
            return jsonify({"error": 1001, "msg": "圖片格式僅限 png、PNG、jpg、JPG、bmp"})
 
        user_input = request.form.get("name")
 
        # 當前文件所在路徑
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))        
        f.save(upload_path)
 
        # 使用轉換opencv轉換圖片格式、名稱
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)

        result, point = predict(img_path=basepath+'/static/images/test.jpg', model=model)

        return render_template('upload_ok.html',result=result, point=point, val1=time.time())
 
    return render_template('upload.html')
 
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8987, debug=True)
