import os
from flask import Flask, render_template, request, g, redirect, url_for, send_from_directory, session
import sqlite3
from werkzeug import secure_filename
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

import models

# Settings
app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db.sqlite3'),
    SECRET_KEY='foo-baa',
))

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cifar10_labels = np.array([
    'airplane',
    'automobile',
    'bird',
    'cat',
    'deer',
    'dog',
    'frog',
    'horse',
    'ship',
    'truck'])

model = load_model('./cifar10_cnn.h5')

# 以下、DB接続関連の関数
 
def connect_db():
    """ データベース接続に接続します """
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con
 
 
def get_db():
    """ connectionを取得します """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
 
 
@app.teardown_appcontext
def close_db(error):
    """ db接続をcloseします """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# methods
def allowed_file(filename):
    '''
    v0.0.0
    content:
        Verify extension
    Input:
        file name
    Output:
        True or False
    '''
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def resize_upload_img(img_name):
    '''
    v0.0.0
    content:
        resize image and replace to array
    Input:
        img_name
    Output:
        array
    '''
    input_img_row = Image.open('./uploads/' + img_name)
    input_img_resize = input_img_row.resize((32,32))
    input_img = np.array(input_img_resize)
    input_img = input_img.astype('float32') / 255
    input_img = input_img[np.newaxis,:,:]

    return input_img

# def classify(input_img):
#     if input_img != None:
#         img_predict(input_img)
        
import tensorflow as tf
graph = tf.get_default_graph()
def img_predict(input_img):
    '''
    v0.0.0
    content:
        predict input image
    Input:
        input image array
    Output:
        predict results
    '''
    input_run = resize_upload_img('bird1.jpg')
    model.predict_proba(input_run)
    print(input_img.shape)
    y_pred = model.predict(input_img)
    y_proba = model.predict_proba(input_img)
    # y = y_pred[0].argmax()
    return y_pred[0].argmax(), cifar10_labels[np.argmax(y_pred[0])] \
            ,y_proba[0][y_proba[0].argsort()[::1]],cifar10_labels[y_proba[0].argsort()[::1]] 

# feature
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        img_file = request.files['img_file']
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = '/uploads/' + filename
            input_img = resize_upload_img(filename)
            # global graph
            # with graph.as_default():
            [results_pred, results_label, results_proba, results_probalabel] = \
                img_predict(input_img)
            return render_template('index.html', img_url=img_url)
        else:
            return render_template('index.html', img_url="")
    else:
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.debug = True
    app.run()