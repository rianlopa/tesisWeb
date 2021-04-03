import os
from flask import Flask, flash, make_response, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import numpy as np
import cv2
from mainDetector import glass_detector

UPLOAD_FOLDER = r'C:/Users/rianl/Desktop/tensorflow-yolov4-tflite/uploadFolder'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'pic' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['pic']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = app.config['UPLOAD_FOLDER'] + '/' + filename
            img = cv2.imread(path)
            dimensions = img.shape
            altura = dimensions[0]
            anchura = dimensions[1]
            pathTs = './uploadFolder/' + filename
            glass_detector(img, filename)
            print(altura)
            print(anchura)
            labeledTs = 'label' + filename
            #return redirect(url_for('uploaded_file', filename=filename))
            return render_template("draw.html", image_name=labeledTs, imgHeight=altura, imgWidth=anchura)
    return "Hello world"

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("uploadFolder", filename)

@app.route('/load/<imagen>', methods=['GET', 'POST'])
def load(imagen):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'archivo' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['archivo']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = app.config['UPLOAD_FOLDER'] + '/' + imagen
            img = cv2.imread(path)
            dimensions = img.shape
            altura = dimensions[0]
            anchura = dimensions[1]
            #return redirect(url_for('uploaded_file', filename=filename))
            return render_template("filed.html", file_name=filename, image_name=imagen, imgHeight=altura, imgWidth=anchura)
    return "Hello world algo no esta bien"

@app.route('/load/file/<filename>')
def send_file(filename):
    return send_from_directory("uploadFolder", filename)

'''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    path = app.config['UPLOAD_FOLDER'] + '/' + filename
    img = cv2.imread(path)
    ret, jpeg = cv2.imencode('.jpg', img)
    response = make_response(jpeg.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response
'''

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0')