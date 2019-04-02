# coding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

# 配置数据库连接配置
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1:3306/pyvideos"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


# 用户模型(继承db.Model)
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    nickname = db.Column(db.String(100), unique=True)   # 昵称
    username = db.Column(db.String(100), unique=True)   # 用户名
    password = db.Column(db.String(100))                # 密码
    email = db.Column(db.String(100), unique=True)      # 邮箱
    phone = db.Column(db.String(11), unique=True)       # 手机号码
    info = db.Column(db.Text)                           # 个性简介
    avatar = db.Column(db.String(255))                  # 头像
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)   # 注册时间
    uuid = db.Column(db.String(255), unique=True)       # 唯一标识

    def __repr__(self):
        return "<User %r>" % self.id


# 用户登录日志模型
class UserLog(db.Model):
    __tablename__ = "user_log"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    user_id = db.Column(db.BigInteger)                  # 关联的用户id
    ip = db.Column(db.String(100))                      # 登录ip
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)   # 创建时间（即用户登录时间）

    def __repr__(self):
        return "<UserLog %r>" % self.id


# 视频标签模型
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    name = db.Column(db.String(100), unique=True)       # 标签名称
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间

    def __repr__(self):
        return "<Tag %r>" % self.name


# 视频模型
class Video(db.Model):
    __tablename__ = "video"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    title = db.Column(db.String(255), unique=True)      # 标题
    url = db.Column(db.String(255), unique=True)        # 路径
    info = db.Column(db.Text)                           # 简介
    logo = db.Column(db.String(255), unique=True)       # logo/缩略图
    star = db.Column(db.SmallInteger)                   # 星级
    play_amount = db.Column(db.BigInteger)              # 播放量
    comment_amount = db.Column(db.BigInteger)           # 评论量
    tag_id = db.Column(db.BigInteger)                   # 所属的标签id
    area = db.Column(db.String(50), default="")         # 地区
    release_time = db.Column(db.Date)                   # 发布日期
    length = db.Column(db.String(100))                  # 时长
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间

    def __repr__(self):
        return "<Video %r>" % self.title


# 视频预告模型
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    title = db.Column(db.String(255), unique=True)      # 标签名称
    logo = db.Column(db.String(255), unique=True)       # logo/缩略图
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间

    def __repr__(self):
        return "<Preview %r>" % self.title


# 评论模型
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    content = db.Column(db.Text)                        # 评论内容
    video_id = db.Column(db.BigInteger)                 # 评论的视频id
    user_id = db.Column(db.BigInteger)                  # 评论的用户id
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间（即评论时间）

    def __repr__(self):
        return "<Comment %r>" % self.id


# 收藏模型
class Collection(db.Model):
    __tablename__ = "collection"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    video_id = db.Column(db.BigInteger)                 # 收藏的视频id
    user_id = db.Column(db.BigInteger)                  # 收藏的用户id
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间（即收藏时间）

    def __repr__(self):
        return "<Collection %r>" % self.id


# 用户权限模型
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    name = db.Column(db.String(100), unique=True)       # 名称
    url = db.Column(db.String(100), unique=True)        # 路由
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间（即收藏时间）

    def __repr__(self):
        return "<Auth %r>" % self.name


# 用户角色模型
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    name = db.Column(db.String(100), unique=True)       # 名称
    auth_set = db.Column(db.String(600))                # 路由
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间（即收藏时间）

    def __repr__(self):
        return "<Role %r>" % self.name







