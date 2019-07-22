from flask import Flask, render_template, url_for, request, jsonify, redirect
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)  # app = Flask("my-app", static_folder="path1", template_folder="path2")


@app.route("/")
def my_echartes():
    return render_template("index.html")


@app.route("/home")
def my_home():
    return render_template("login.html")


@app.route("/args/")
def demo_args():
    print("path:%s" % request.path)
    print("full path:%s" % request.full_path)
    p = request.args.get('p')
    p_lst = request.args.getlist("p")
    if p == None:
        print("None")
    else:
        print("p=%s" % p)
    print(request.args.__str__())
    return request.args.__str__()


# ------------
#
# ------------

@app.route('/register', methods=['POST'])
def redister():
    print("headers:%s\n" % request.headers)
    print("read:%s\n" % request.stream.read())
    print("form:%s\n" % request.form)
    return 'welcome'


# ------------
# 传递参数
# ------------
@app.route("/hello/<name>")
def hello_name(name):
    print("name:%s" % name)
    return jsonify(namedai=name)  # 返回 {"namedai":"dai"}


# ------------
# 跳转
# ------------
@app.route("/success/<name>")
def success(name):
    return "welcome %s" % name


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form['nm']
        return redirect(url_for("success", name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))


# ------------
# 文件上传 https://www.w3cschool.cn/flask/flask_file_uploading.html
# ------------
UPLOAD_FOLDER = 'E:/test_uploads'
ALLOWED_EXTENSIONS = set(["csv", 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route("/uploader", methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        f = request.files['file']
        print("file_name:%s" % f.filename)
        secure_name = secure_filename(f.filename)  # 文件保存
        print("secure_name:%s" %secure_name)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        return 'file uploaded successfully'


if __name__ == "__main__":
    app.run(port=5660)
