from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = './static/uploads'  # 上传文件到这里
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'jpeg'}  # 允许的格式,保证安全性
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制文件大小


# 允许的文件格式
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        plan_file = request.files['plan']
        list_file = request.files['name_list']
        if plan_file and allowed_file(plan_file.filename):
            plan_filename = 'plan.' + plan_file.filename.rsplit('.', 1)[1]
            # filename = request.form['filename']
            # filename = str(filename)
            plan_file.save(os.path.join(app.config['UPLOAD_FOLDER'], plan_filename))
            # return redirect(url_for('uploaded_file', filename=filename))
        if list_file and allowed_file(list_file.filename):
            list_filename = 'list.' + list_file.filename.rsplit('.', 1)[1]
            list_file.save(os.path.join(app.config['UPLOAD_FOLDER'], list_filename))
    return render_template("upload.html")


if __name__ == '__main__':
    app.run()
