from flask import Flask, render_template, url_for, request

app = Flask(__name__)  # app = Flask("my-app", static_folder="path1", template_folder="path2")

import sqlite3
from flask import Flask, request, render_template, jsonify
import sys
from server.show_data import ShowData

app = Flask(__name__)


def get_db():
    db = sqlite3.connect('mydb.db')
    db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    rv = cur.fetchall()
    db.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/active_days", methods=["GET"])
def active_days():
    return render_template("active_days.html")


@app.route("/days_data", methods=["GET"])
def days_data():
    '''
    获取数据
    :return:
    '''
    if request.method == "GET":
        days = ["一天", "二天", "三天", "四天", "五天", "六天", "七天", "其他"]
        num = [142, 256, 456, 12, 89, 41, 232, 122]
        res = jsonify(days=days, num=num)
    return res


@app.route("/entropy", methods=["GET"])
def entropy():
    return render_template("entropy.html")


@app.route("/entropy_data", methods=["GET"])
def entropy_data():
    '''
    [9, 267, 216, 280, 4.8, 108, 64, "重度污染"]
    [日期（横坐标值）9，纵坐标值267，PM2.5 :216, ..., 二氧化硫：64， 标签]
    [area, text, name, time, newsid]
    '''
    dataBJ = ShowData().fanchengcheng_entropy_data() # 范丞丞事件
    dataZhang = ShowData().zhangdanfeng_entropy_data() # 张丹峰事件
    res = jsonify(dataBJ=dataBJ, dataZhang=dataZhang)
    return res


@app.route("/attention", methods=["GET"])
def attention():
    return render_template("news_attention.html")


@app.route("/attention_data", methods=["GET"])
def attention_data():
    nums = ["一天", "二天", "三天", "四天", "五天", "六天", "七天", "其他"]
    users = [142, 256, 456, 12, 89, 41, 232, 122]
    res = jsonify(nums=nums, users=users)
    return res


@app.route("/semantic", methods=["GET"])
def semantic():
    return render_template("semantic_repetition_rate.html")


@app.route("/semantic_data", methods=["GET"])
def semantic_data():
    xData = ['8:00-10:00', '10:00-12:00', '12:00-14:00', '14:00-16:00', '16:00-18:00'];
    yData = [80, 87, 51, 81, 23, 45, 33];
    res = jsonify(xData=xData,yData=yData)
    return res


@app.route("/weather", methods=["GET"])
def weather():
    if request.method == "GET":
        res = query_db("SELECT * FROM weather")
        res = jsonify(month=[x[0] for x in res],
                      evaporation=[x[1] for x in res],
                      precipitation=[x[2] for x in res])
        print(res)
    return res


@app.route('/map')
def map():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5660, debug=True)
