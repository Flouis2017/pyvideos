# coding:utf8
from . import admin
from flask import render_template, redirect, url_for


@admin.route("/")
def index():
    return render_template("admin/index.html")


@admin.route("/login/")
def login():
    return render_template("admin/login.html")


@admin.route("/logout/")
def logout():
    return redirect(url_for("admin.login"))


@admin.route("/pwd/")
def pwd():
    return render_template("admin/pwd.html")


@admin.route("/tag_add/")
def tag_add():
    return render_template("admin/tag_add.html")


@admin.route("/tag_list/")
def tag_list():
    return render_template("admin/tag_list.html")


@admin.route("/video_add/")
def video_add():
    return render_template("admin/video_add.html")


@admin.route("/video_list/")
def video_list():
    return render_template("admin/video_list.html")


@admin.route("/preview_add/")
def preview_add():
    return render_template("admin/preview_add.html")


@admin.route("/preview_list/")
def preview_list():
    return render_template("admin/preview_list.html")


@admin.route("/user_list/")
def user_list():
    return render_template("admin/user_list.html")


@admin.route("/user_view/")
def user_view():
    return render_template("admin/user_view.html")


@admin.route("/comment_list/")
def comment_list():
    return render_template("admin/comment_list.html")


@admin.route("/collection_list/")
def collection_list():
    return render_template("admin/collection_list.html")


@admin.route("/admin_op_log_list/")
def admin_op_log_list():
    return render_template("admin/admin_op_log_list.html")


@admin.route("/admin_login_log_list/")
def admin_login_log_list():
    return render_template("admin/admin_login_log_list.html")


@admin.route("/login_log_list/")
def login_log_list():
    return render_template("admin/login_log_list.html")


@admin.route("/auth_add/")
def auth_add():
    return render_template("admin/auth_add.html")


@admin.route("/auth_list/")
def auth_list():
    return render_template("admin/auth_list.html")


@admin.route("/role_add/")
def role_add():
    return render_template("admin/role_add.html")


@admin.route("/role_list/")
def role_list():
    return render_template("admin/role_list.html")


@admin.route("/admin_user_add/")
def admin_user_add():
    return render_template("admin/admin_user_add.html")


@admin.route("/admin_user_list/")
def admin_user_list():
    return render_template("admin/admin_user_list.html")





