# coding:utf8
from . import home
from flask import render_template, redirect, url_for, flash, request, session
from app.home.forms import *
from app.models import User, LoginLog, Preview, Tag, Video, Comment
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from app import db, app
import uuid
from functools import wraps
from sqlalchemy import or_
import os
import datetime


# 登录拦截器(注意装饰器的写法)
def login_req(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorator


# 修改文件名称
def change_filename(filename):
    file_info = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + file_info[-1]
    return filename


# 删除文件
def del_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


# 首页(需要对视频按照标签/星级/上映时间/播放数量和评论数量进行展示)
@home.route("/", methods=["GET"])
def index():
    tags = Tag.query.all()
    tid = int(request.args.get("tid", 0))
    star = int(request.args.get("star", 0))
    # 上映时间排序：0：最近 1：更早
    time = int(request.args.get("time", 0))
    # 播放/评论数量排序：0：从高到低 1：从低到高
    po = int(request.args.get("po", 0))
    co = int(request.args.get("co", 0))

    # 填充筛选条件字典
    param = dict(
        tid=tid,
        star=star,
        # 发布时间排序：0：最近 1：更早
        time=time,
        # 播放/评论数量排序：0：从高到低 1：从低到高
        po=po,
        co=co
    )

    # 条件查询
    page_data = Video.query
    if tid != 0:
        page_data = page_data.filter(Video.tag_id == tid)
    if star != 0:
        page_data = page_data.filter(Video.star == star)
    if time != 0:
        if time == 1:
            page_data = page_data.order_by(Video.release_time.desc())
        else:
            page_data = page_data.order_by(Video.release_time.asc())
    if po != 0:
        if po == 1:
            page_data = page_data.order_by(Video.play_amount.desc())
        else:
            page_data = page_data.order_by(Video.play_amount.asc())
    if co != 0:
        if co == 1:
            page_data = page_data.order_by(Video.comment_amount.desc())
        else:
            page_data = page_data.order_by(Video.comment_amount.asc())

    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))

    page_data = page_data.paginate(page=page, per_page=size)

    return render_template("home/index.html", tags=tags, param=param, page_data=page_data)


# (预告)轮播图
@home.route("/banner", methods=["GET", "POST"])
def banner():
    data = Preview.query.all()
    return render_template("home/banner.html", data=data)


# 视频搜索
@home.route("/search", methods=["GET", "POST"])
def search():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    key_word = request.args.get("key_word", "")
    page_data = Video.query.filter(Video.title.like("%" + key_word + "%"))\
        .order_by(Video.play_amount.desc()).paginate(page=page, per_page=size)
    return render_template("home/search.html", page_data=page_data, key_word=key_word)


# 会员登录
@home.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        account = data["account"]
        pwd = data["pwd"]
        user = User.query.filter(or_(User.username == account, User.email == account, User.phone == account)).first()
        if user is None:
            flash("该账号不存在！", "err")
            return redirect(url_for("home.login"))
        if not user.check_pwd(pwd):
            flash("密码出错！", "err")
            return redirect(url_for("home.login"))
        session["username"] = user.username
        session["user_id"] = user.id

        # 登录日志
        login_log = LoginLog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(login_log)
        db.session.commit()
        return redirect(url_for("home.user"))
    return render_template("home/login.html", form=form)


@home.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect(url_for("home.login"))


# 会员注册
@home.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            data = form.data
            new_user = User(
                username=data["username"],
                email=data["email"],
                phone=data["phone"],
                pwd=generate_password_hash(data["pwd"]),
                avatar="default.png",
                uuid=uuid.uuid4().hex
            )
            db.session.add(new_user)
            db.session.commit()
            flash("注册成功", "ok")
        except Exception as e:
            print(e)
            flash("服务器异常，注册失败！", "err")
    return render_template("home/register.html", form=form)


# 会员中心(编辑个人资料)
@home.route("/user", methods=["GET", "POST"])
@login_req
def user():
    cur_user = User.query.get_or_404(int(session["user_id"]))
    if cur_user.avatar is None:
        cur_user.avatar = "default.png"
    form = UserDetailForm()
    if request.method == "GET":
        form.info.data = cur_user.info
    if form.validate_on_submit():
        try:
            data = form.data

            # 邮箱去重校验
            email = data["email"]
            cnt = User.query.filter_by(email=email).count()
            if cnt >= 1 and cur_user.email != email:
                flash("邮箱已被其他会员使用！", "err")
                return redirect(url_for("home.user"))

            # 手机去重校验
            phone = data["phone"]
            cnt = User.query.filter_by(phone=phone).count()
            if cnt >= 1 and cur_user.phone != phone:
                flash("手机已被其他会员绑定！", "err")
                return redirect(url_for("home.user"))

            # 更新会员头像
            avatar_up_dir = app.config["UP_DIR"] + "/avatar"
            if not os.path.exists(avatar_up_dir):
                os.makedirs(avatar_up_dir)
            if form.avatar.data.filename != "":
                if cur_user.avatar != "default.png":
                    del_file(avatar_up_dir + "/" + cur_user.avatar)
                avatar_filename = secure_filename(form.avatar.data.filename)
                cur_user.avatar = change_filename(avatar_filename)
                form.avatar.data.save(avatar_up_dir + "/" + cur_user.avatar)

            # 数据库落地
            cur_user.email = email
            cur_user.phone = phone
            cur_user.info = data["info"]
            db.session.add(cur_user)
            db.session.commit()
            flash("保存成功", "ok")
        except Exception as e:
            print(e)
            flash("服务器异常，操作失败！", "err")
        return redirect(url_for("home.user"))
    return render_template("home/user.html", form=form, cur_user=cur_user)


@home.route("/pwd", methods=["GET", "POST"])
@login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        try:
            data = form.data
            # xx = User.query.filter(User.id == session["user_id"])
            # print(type(xx))     # BaseQuery
            # 获取当前会员用户
            cur_user = User.query.filter(User.id == session["user_id"]).first()
            # 对新密码加密
            cur_user.pwd = generate_password_hash(data["newpwd"])
            # 数据库落地
            db.session.add(cur_user)
            db.session.commit()
            flash("操作成功", "ok")
        except Exception as e:
            print(e)
            flash("服务器异常，操作失败！", "err")
        return redirect(url_for("home.pwd"))
    return render_template("home/pwd.html", form=form)


# 会员用户评论
@home.route("/comment", methods=["GET", "POST"])
@login_req
def comment():
    return render_template("home/comment.html")


@home.route("/login_log", methods=["GET", "POST"])
@login_req
def login_log():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    # 分页查询
    page_data = LoginLog.query.filter(LoginLog.user_id == session["user_id"])\
                        .order_by(LoginLog.id.desc())\
                        .paginate(page=page, per_page=size)
    return render_template("home/login_log.html", page_data=page_data)


# 会员用户收藏
@home.route("/collection", methods=["GET", "POST"])
@login_req
def collection():
    return render_template("home/collection.html")


@home.route("/play", methods=["GET", "POST"])
def play():
    # 根据视频主键id获取视频
    vid = int(request.args.get("vid", 0))
    video = Video.query.get_or_404(vid)
    tag = Tag.query.filter(Tag.id == video.tag_id).first()

    # 播放数量加一：
    video.play_amount = video.play_amount + 1
    db.session.add(video)
    db.session.commit()

    form = CommentForm()
    if "username" in session and form.validate_on_submit():
        try:
            data = form.data
            new_comment = Comment(
                content=data["content"],
                video_id=vid,
                user_id=session["user_id"]
            )
            db.session.add(new_comment)
            db.session.commit()
            # 评论数加一
            video.comment_amount = video.comment_amount + 1
            db.session.add(video)
            db.session.commit()
            flash("评论成功", "ok")
        except Exception as e:
            print(e)
            flash("服务器异常，评论失败！", "err")
        return redirect(url_for("home.play", vid=vid))

    # 分页查询评论列表
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    page_data = db.session.query(User.avatar, User.username, Comment.create_time, Comment.content) \
        .join(User, User.id == Comment.user_id).filter(Comment.video_id == vid) \
        .order_by(Comment.id.desc()).paginate(page=page, per_page=size)

    return render_template("home/play.html", video=video, tag=tag, form=form, page_data=page_data)


