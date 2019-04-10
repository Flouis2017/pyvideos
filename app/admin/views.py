# coding:utf8
from . import admin
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm
from app.models import AdminUser
from functools import wraps


# 登录拦截器(注意装饰器的写法)
def admin_login_req(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorator


@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")


@admin.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin_user = AdminUser.query.filter_by(username=data["username"]).first()
        if not admin_user.check_pwd(data["pwd"]):
            flash("密码错误！")
            return redirect(url_for("admin.login"))

        session["username"] = data["username"]
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


@admin.route("/logout/")
@admin_login_req
def logout():
    session.pop("username", None)
    return redirect(url_for("admin.login"))


@admin.route("/pwd/")
@admin_login_req
def pwd():
    return render_template("admin/pwd.html")


@admin.route("/tag_add/")
@admin_login_req
def tag_add():
    return render_template("admin/tag_add.html")


@admin.route("/tag_list/")
@admin_login_req
def tag_list():
    return render_template("admin/tag_list.html")


@admin.route("/video_add/")
@admin_login_req
def video_add():
    return render_template("admin/video_add.html")


@admin.route("/video_list/")
@admin_login_req
def video_list():
    return render_template("admin/video_list.html")


@admin.route("/preview_add/")
@admin_login_req
def preview_add():
    return render_template("admin/preview_add.html")


@admin.route("/preview_list/")
@admin_login_req
def preview_list():
    return render_template("admin/preview_list.html")


@admin.route("/user_list/")
@admin_login_req
def user_list():
    return render_template("admin/user_list.html")


@admin.route("/user_view/")
@admin_login_req
def user_view():
    return render_template("admin/user_view.html")


@admin.route("/comment_list/")
@admin_login_req
def comment_list():
    return render_template("admin/comment_list.html")


@admin.route("/collection_list/")
@admin_login_req
def collection_list():
    return render_template("admin/collection_list.html")


@admin.route("/admin_op_log_list/")
@admin_login_req
def admin_op_log_list():
    return render_template("admin/admin_op_log_list.html")


@admin.route("/admin_login_log_list/")
@admin_login_req
def admin_login_log_list():
    return render_template("admin/admin_login_log_list.html")


@admin.route("/login_log_list/")
@admin_login_req
def login_log_list():
    return render_template("admin/login_log_list.html")


@admin.route("/auth_add/")
@admin_login_req
def auth_add():
    return render_template("admin/auth_add.html")


@admin.route("/auth_list/")
@admin_login_req
def auth_list():
    return render_template("admin/auth_list.html")


@admin.route("/role_add/")
@admin_login_req
def role_add():
    return render_template("admin/role_add.html")


@admin.route("/role_list/")
@admin_login_req
def role_list():
    return render_template("admin/role_list.html")


@admin.route("/admin_user_add/")
@admin_login_req
def admin_user_add():
    return render_template("admin/admin_user_add.html")


@admin.route("/admin_user_list/")
@admin_login_req
def admin_user_list():
    return render_template("admin/admin_user_list.html")





