# -*- coding: utf-8 -*-
"""
Created on Thu May 10 08:50:45 2018

@author: TobeyWang
"""

import os
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import send_from_directory,Response,session
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER =os.path.join('static', 'upload') 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] =  os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'

def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
@app.route('/')
def index():
    return render_template('index.html')
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('success')
            return redirect(url_for('show',
                                    filename=filename))
    else:
          return render_template('index.html')       
@app.route('/<filename>')
def show(filename):
#    return send_from_directory(app.config['UPLOAD_FOLDER'],
#                               filename)
#    photo = Photo.load(id)
#    #file is exist
#    if photo is None:
#        flash('file is not exist')
#    url = photos.url(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return render_template('index.html',filemessage=full_filename)  
    
if __name__ == '__main__':
 app.run(host='127.0.0.1', port=5000, debug=True)
 