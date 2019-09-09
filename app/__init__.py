# coding:utf8
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# 设置json编码，主要用在前后端交互时中文的显示
app.config['JSON_AS_ASCII'] = False

# 配置数据库连接配置
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Flp8084175@212.64.7.214:3306/pyvideos"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1:3306/pyvideos"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = '22e7de005efe42179caef02d6abf0474'

app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/upload")

# app.debug = True
app.debug = False
db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

# 注册蓝图，相当于SpringMVC中配置ServletDispatcher
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error/404.html"), 404
