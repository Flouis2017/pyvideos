# coding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# 配置数据库连接配置
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1:3306/pyvideos"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

# 会员模型(继承db.Model)
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)        # 主键
    nickname = db.Column(db.String(100), unique=True)   # 昵称
    username = db.Column(db.String(100), unique=True)   # 用户名
    password = db.Column(db.String(100))                # 密码
    email = db.Column(db.String(100), unique=True)      # 邮箱
    phone = db.Column(db.String(11), unique=True)       # 手机号码
    info = db.Column(db.Text)                           # 个性简介
    avatar = db.Column(db.String(255))                  # 头像
    createtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 注册时间
    uuid = db.Column(db.String(255), unique=True)       # 唯一标识
    userlogs = db.relationship('Userlog',backref='user')# 会员日志外键关系

    def __repr__(self):
        return "<User %r>" % self.id

# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)        # 主键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 关联的会员id
    ip = db.Column(db.String(100))                      # 登录ip
    createtime = db.Column(db.DateTime, index=True, default=datetime.now) # 登录时间

    def __repr__(self):
        return "<Userlog %r>" % self.id
