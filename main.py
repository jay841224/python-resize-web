from flask import Flask, render_template, redirect, url_for, request, session
from flask import flash, jsonify
from datetime import timedelta
from werkzeug.utils import secure_filename
from google.cloud import storage
import cv2
import os, time

app = Flask(__name__)
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
app.secret_key = 'jay011089'
app.permanent_session_lifetime = timedelta(minutes=600)
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@app.route('/main', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        rootimg = request.files.get('rootimg')
        # basepath = os.path.dirname(__file__) # 當前文件路徑
        # uploadpath = os.path.join(basepath, 'static/images', 'test.jpg')

        # Create a Cloud Storage client.
        gcs = storage.Client()

        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
        bucket2 = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

        # Create a new blob and upload the file's content.
        blob = bucket.blob(rootimg.filename)
        blob.upload_from_string(rootimg.read(),content_type=rootimg.content_type)
        read = bucket2.get_blob('mico.jpg')
        '''
        img = cv2.imread(uploadpath)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img) #save image

        h, w, s = img.shape
        session['size'] = [w, h]
        rootSize = session['size']

        #from work_img import resizeImg
        #img = resizeImg()
        return render_template('main.html', val1=time.time(), maxwidth=rootSize[0], maxheight=rootSize[1])
        '''
        return read.public_url
    return render_template('home.html')


@app.route('/work', methods=['POST', 'GET'])
def work():
    if request.method == 'POST':
        width = int(request.form['width'])
        height = int(request.form['height'])
        basepath = os.path.dirname(__file__)
        uploadpath = os.path.join(basepath, 'static/images', 'test.jpg')

        #決定html中 img的width height
        rootSize = session['size']
        from work_img import html_img_size
        outputWidth = html_img_size(rootSize, width)


        from work_img import resizeImg
        rootimg = cv2.imread(uploadpath)
        img = resizeImg(rootimg, width, height)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'output.jpg'), img)
        return render_template('main.html', val1=time.time(), val2=time.time(), outputWidthpersent=outputWidth, maxwidth=rootSize[0], maxheight=rootSize[1], outputsize=[width, height]) #max 限制resize的最大值 不可超出原圖
    return jsonify('false')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)