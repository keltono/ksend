#! /usr/bin/env python

from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import os
import string
import random

UPLOAD_FOLDER = "/mnt/.share"
HOSTNAME = "https://keltono.net/"
PORT = 3982

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER',UPLOAD_FOLDER)
app.config['HOSTNAME'] = os.environ.get('HOSTNAME',HOSTNAME)
app.config['PORT'] = int(os.environ.get('PORT',PORT))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() not in ["php","html"]

def getRandomChars():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

@app.route("/", methods=['GET'])
def index():
    render_template('templates/index.html')

@app.route("/", methods=['POST'])
def file_upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename =  '.' + getRandomChars() + '_' + secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        forward = app.config['HOSTNAME'] + '.share/' + filename
        print(forward)
        return redirect(forward)

# @app.route('/.share/<filename>')
# def uploaded_file(filename):
    # return redirect(app.config['HOSTNAME'] +)
    # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def run():
    app.run("0.0.0.0", app.config['PORT'])

if __name__ == "__main__":
    run()
