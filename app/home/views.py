# coding:utf8
from . import home
from flask import render_template, redirect, url_for, flash, request, session
from app.home.forms import *
from app.models import User, LoginLog
from werkzeug.security import generate_password_hash
from app import db
import uuid
from functools import wraps
from sqlalchemy import or_


# 登录拦截器(注意装饰器的写法)
def login_req(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorator


@home.route("/")
def index():
    return render_template("home/index.html")


@home.route("/banner/")
def banner():
    return render_template("home/banner.html")


@home.route("/search/")
def search():
    return render_template("home/search.html")


@home.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        account = data["account"]
        pwd = data["pwd"]
        user = User.query.filter(or_(User.username == account, User.email == account, User.phone == account)).first()
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


@home.route("/logout/")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect(url_for("home.login"))


# 会员注册
@home.route("/register/", methods=["GET", "POST"])
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
                uuid=uuid.uuid4().hex
            )
            db.session.add(new_user)
            db.session.commit()
            flash("注册成功", "ok")
        except Exception as e:
            print(e)
            flash("服务器异常，注册失败！", "err")
    return render_template("home/register.html", form=form)


@home.route("/user/")
@login_req
def user():
    return render_template("home/user.html")


@home.route("/pwd/")
@login_req
def pwd():
    return render_template("home/pwd.html")


@home.route("/comment/")
@login_req
def comment():
    return render_template("home/comment.html")


@home.route("/login_log/")
@login_req
def login_log():
    return render_template("home/login_log.html")


@home.route("/collection/")
@login_req
def collection():
    return render_template("home/collection.html")


@home.route("/play")
@login_req
def play():
    return render_template("home/play.html")


