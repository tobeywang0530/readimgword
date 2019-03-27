# -*- coding: utf-8 -*-
"""
Created on Thu May 10 08:50:45 2018

@author: TobeyWang
"""

import os
import sys
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import send_from_directory,jsonify,Response,session
from werkzeug.utils import secure_filename


app = Flask(__name__)

UPLOAD_FOLDER =os.path.join('static', 'upload') 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
OCR_FOLDER =os.path.join('static', 'Tesseract-OCR') 

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
from PIL import Image
import pytesseract as ocr 
@app.route('/_scan')
def scan():
    filename = request.args.get('filename', 0, type=str)
    full_text=''
    if(filename!=''):
        try:
            ocr.pytesseract.tesseract_cmd =OCR_FOLDER+ r'\tesseract.exe'
            tessdata_dir_config = '--tessdata-dir "'+OCR_FOLDER+'\\tessdata"'
            #get file
            #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            full_filename=filename
            img = Image.open(full_filename)
            full_text=ocr.image_to_string(img, lang='chi_tra',config=tessdata_dir_config)
        except Exception as e:
            full_text='can not reading this image--'+filename+' error--'+str(e)
    else:
        full_text='no file name '
    return jsonify(result=full_text)
#    return render_template('index.html',textmessage=full_text)  
if __name__ == '__main__':
 app.run(host='127.0.0.1', port=8000, debug=True)
 