import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Settings
app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

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
    input_img_resize = input_img_row.resize((500,500))
    input_img = np.array(input_img_resize)
    input_img = input_img.astype('float32') / 255
    input_img = input_img[np.newaxis,:,:]

    return input_img
    
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
            return render_template('index.html', img_url=img_url)
        else:
            return ''' <p>許可されていない拡張子です</p> '''
    else:
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename), resize_upload_img(filename)

if __name__ == '__main__':
    app.debug = True
    app.run()