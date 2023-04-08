from keras.models import load_model
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import time
from datetime import timedelta
from predict import predict


app = Flask(__name__)

# 緩存過期時間
app.send_file_max_age_default = timedelta(seconds=5)
# 啟動網頁應用程式時就先載入預測模型
model = load_model('model/26-0.12.h5')

# 設定允許的圖片格式
ALLOWED_EXTENSIONS = ('png', 'jpg', 'JPG', 'jpeg', 'JPEG', 'PNG', 'bmp')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# route
@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        # 如果用戶上傳了不允許的圖片格式，在瀏覽器顯示錯誤訊息
        if not (f and allowed_file(f.filename)):
            return "Upload image format is limited to png, JPG, jpeg, JPEG, JPG or bmp."

        user_input = request.form.get("name")

        # 將用戶上傳的圖片儲存到當前目錄下 static/images/
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, 'static/images', f.filename)
        f.save(upload_path)

        # 預測用戶上傳的照片評分，並將結果、分數傳進上傳OK的模板顯示
        result, point = predict(model, img_path=upload_path)
        return render_template('upload_ok.html',filename=f.filename ,result=result, point=point, val1=time.time())

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8987)
