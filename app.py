# -*- coding: utf-8 -*-
#
# Mai Xuan Trang
# Flask application
#
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from sgoogle.googleindexchecker import IndexChecker
from datetime import datetime
import sys
from werkzeug.utils import secure_filename

reload(sys)  
sys.setdefaultencoding('utf8')

ALLOWED_EXTENSIONS = set(['txt'])
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/googleindexchecker')
def show_index_checker():
    return render_template('index_check.html')


@app.route('/googleindexchecker', methods=['POST'])
def check_result():
    file = request.files['file']
    if file.filename == '':
        return render_template('index_check.html', error='No selected file')
    
    if not allowed_file(file.filename):
        return render_template('index_check.html', error='File type is not supported')
    
    if file and allowed_file(file.filename):
        urlstr = file.read()
        urls = urlstr.split()
        if len(urls) > 200:
            return render_template('index_check.html', error='The file contains a large number of URLs. The checking process may get block by Google. The file should contain not exceed 200 URLs.')
        else:
            checker = IndexChecker(urls, tld="co.jp", use_proxy=True)
            urlchecked = checker.check_solenium_remote()
            return render_template('index_check.html', urlindexchecks=urlchecked)

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)