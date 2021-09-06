#! /usr/bin/env python

from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename
import os
import string
import random
import secrets


#things to change if you are actually going to use this
UPLOAD_FOLDER = "/mnt/.share"
HOSTNAME = "https://keltono.net/"
PORT = 3982

app = Flask(__name__)

secret = secrets.token_urlsafe(32)
app.secret_key = secret

#you could also pass the config information via enviroment variables
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER',UPLOAD_FOLDER)
app.config['HOSTNAME'] = os.environ.get('HOSTNAME',HOSTNAME)
app.config['PORT'] = int(os.environ.get('PORT',PORT))


def allowed_file(filename):
    #(fine if you trust your users (such as if the page is behind http auth that only you have access to), terrible, bad, and stupid every other time)
    return True
    #what you should do if you do not vet users
    #return '.' in filename and filename.rsplit('.', 1)[1].lower() not in ["php","html"]

#psuedorandom, which is fine
def getRandomChars():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

#check if the upload is valid
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
        share_link = app.config['HOSTNAME'] + '.share/' + filename
        return render_template('success.html',share_link=share_link)

#same as the function above, just returning a json instead (for use in mobile/etc)
@app.route("/json",methods=['POST'])
def file_upload_mobile():
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({"failed" : True, "failure_reason" : "no file", "file_url": ""})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"failed" : True, "failure_reason" : "no selected file", "file_url": ""})
    if file and allowed_file(file.filename):
        filename =  '.' + getRandomChars() + '_' + secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        share_link = app.config['HOSTNAME'] + '.share/' + filename
        return jsonify({"failed" : False, "failure_reason" : "", "file_url": share_link})

def run():
    app.run("0.0.0.0", app.config['PORT'])

if __name__ == "__main__":
    run()
