from flask import Flask, render_template, redirect, url_for, request, session
from flask import flash, jsonify
from datetime import timedelta
from werkzeug.utils import secure_filename
from google.cloud import storage
import cv2
import os, time
import numpy as np

app = Flask(__name__)
CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
app.secret_key = 'jay011089'
app.permanent_session_lifetime = timedelta(minutes=100)
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@app.route('/main', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        t = ''
        t = t.join(str(time.time()).split('.'))
        session['time'] = t
        rootimg = request.files.get('rootimg')

        # Create a Cloud Storage client.
        gcs = storage.Client()

        # Get the bucket that the file will be uploaded to.
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
        #bucket = gcs.get_bucket('my-resize-project')

        # Create a new blob and upload the file's content.
        blob = bucket.blob('{}root.jpg'.format(session['time']))
        blob.upload_from_string(rootimg.read(),content_type=rootimg.content_type)
        
        #read rootimg and get height and width
        bucket = gcs.get_bucket('my-resize-project')
        read = bucket.get_blob('{}root.jpg'.format(session['time']))
        rootimg = read.download_as_string()
        nparr = np.fromstring(rootimg, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        h, w, s = img.shape
        session['size'] = [w, h]
        rootSize = session['size']

        #from work_img import resizeImg
        #img = resizeImg()
        return render_template('main.html',root_img=blob.public_url, val1=time.time(), maxwidth=rootSize[0], maxheight=rootSize[1])
    return render_template('home.html')


@app.route('/work', methods=['POST', 'GET'])
def work():
    if request.method == 'POST':
        width = int(request.form['width'])
        height = int(request.form['height'])

        #決定html中 img的width height
        rootSize = session['size']
        from work_img import html_img_size
        outputWidth = html_img_size(rootSize, width)


        from work_img import resizeImg
        gcs = storage.Client()
        bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
        #bucket = gcs.get_bucket('my-resize-project')
        read = bucket.get_blob('{}root.jpg'.format(session['time']))
        rootimg = read.download_as_string()
        nparr = np.fromstring(rootimg, np.uint8)
        rootimg = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        rimg = resizeImg(rootimg, width, height)
        s, rimg = cv2.imencode('.jpg', rimg)
        rimg = rimg.tobytes()
        bucket = gcs.get_bucket('my-resize-project')
        blob = bucket.blob('{}rimg.jpg'.format(session['time']))
        blob.upload_from_string(rimg)

        return render_template('main.html', val1=time.time(), val2=time.time(), outputWidthpersent=outputWidth,
        maxwidth=rootSize[0], maxheight=rootSize[1], outputsize=[width, height],
        root_img=read.public_url, rimg=blob.public_url,
        download_link=blob.media_link) #max 限制resize的最大值 不可超出原圖
    return jsonify('false')





if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)