# coding:utf8
from datetime import datetime
from app import db


# 前台数据模型设计
# 用户模型(继承db.Model)
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    username = db.Column(db.String(100), unique=True)   # 用户名
    pwd = db.Column(db.String(100))                     # 密码
    email = db.Column(db.String(100), unique=True)      # 邮箱
    phone = db.Column(db.String(11), unique=True)       # 手机号码
    info = db.Column(db.Text)                           # 个性简介
    avatar = db.Column(db.String(255))                  # 头像
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)   # 注册时间
    uuid = db.Column(db.String(255), unique=True)       # 唯一标识

    def __repr__(self):
        return "<User %r>" % self.id

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 用户登录日志模型
class LoginLog(db.Model):
    __tablename__ = "login_log"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    user_id = db.Column(db.BigInteger)                  # 关联的用户id
    ip = db.Column(db.String(100))                      # 登录ip
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)   # 创建时间（即用户登录时间）

    def __repr__(self):
        return "<LoginLog %r>" % self.id


# 视频标签模型
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    name = db.Column(db.String(100), unique=True)       # 标签名称
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    # videos = db.relationship("Video", backref="video_tag")    # 关联视频模型

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
    # tag_id = db.Column(db.BigInteger, db.ForeignKey("tag.id"))  # 所属的标签id（外键关联）
    tag_id = db.Column(db.BigInteger)                   # 所属的标签id（外键关联）
    area = db.Column(db.String(50), default="")         # 地区
    release_time = db.Column(db.Date)                   # 发布日期
    length = db.Column(db.String(100))                  # 时长
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间

    def __repr__(self):
        return "<Video %r>" % self.title

    @staticmethod
    def get_base_columns_str():
        return " id as id, title as title, url as url, info as info, logo as logo," \
               " star as star, play_amount as play_amount, comment_amount as comment_amount, tag_id as tag_id," \
               " area as area, release_time as release_time, length as length, create_time as create_time "


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


# 后台数据模型设计
# 权限模型
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    name = db.Column(db.String(100), unique=True)       # 名称
    url = db.Column(db.String(100), unique=True)        # 路由
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色模型
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    name = db.Column(db.String(100), unique=True)       # 名称
    auth_set = db.Column(db.String(600))                # 路由(权限主键)集合
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员(用户)模型
class AdminUser(db.Model):
    __tablename__ = "admin_user"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    role_id = db.Column(db.BigInteger)                  # 角色id
    username = db.Column(db.String(100), unique=True)   # 用户名
    pwd = db.Column(db.String(100))                     # 密码
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间

    def __repr__(self):
        return "<AdminUser %r>" % self.id

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 登录日志模型
class AdminLoginLog(db.Model):
    __tablename__ = "admin_login_log"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    admin_user_id = db.Column(db.BigInteger)            # 管理员id
    ip = db.Column(db.String(100))                      # 登录ip
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)   # 创建时间（即登录时间）

    def __repr__(self):
        return "<AdminLoginLog %r>" % self.id


# 操作日志模型
class AdminOpLog(db.Model):
    __tablename__ = "admin_op_log"
    id = db.Column(db.BigInteger, primary_key=True)     # 主键
    admin_user_id = db.Column(db.BigInteger)            # 管理员id
    ip = db.Column(db.String(100))                      # 登录ip
    detail = db.Column(db.String(600))                  # 操作详情
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)   # 创建时间（即操作时间）

    def __repr__(self):
        return "<AdminOpLog %r>" % self.id


# 数据表自动化生成
"""
if __name__ == "__main__":
    # db.create_all()

    # 插入超级管理员角色
    # role = Role(
    #     name="超级管理员",
    #     auth_set=""
    # )
    # db.session.add(role)
    # db.session.commit()

    # 插入管理员
    from werkzeug.security import generate_password_hash
    adminUser = AdminUser(
        role_id=1,
        username="admin",
        pwd=generate_password_hash("123456")
    )
    db.session.add(adminUser)
    db.session.commit()
"""

