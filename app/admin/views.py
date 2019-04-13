# coding:utf8
from . import admin
from flask import render_template, redirect, url_for, flash, session, request, jsonify
from app.admin.forms import *
from app.models import *
from functools import wraps
from app import db
from app.admin.result import ResultEnum


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


# 登录
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


# 退出
@admin.route("/logout/", methods=["GET", "POST"])
@admin_login_req
def logout():
    session.pop("username", None)
    return redirect(url_for("admin.login"))


# 修改密码
@admin.route("/pwd/", methods=["GET", "POST"])
@admin_login_req
def pwd():
    return render_template("admin/pwd.html")


# 添加标签
@admin.route("/tag_add", methods=["GET", "POST"])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        cnt = Tag.query.filter_by(name=data["name"]).count()
        if cnt >= 1:
            flash("已存在！", "err")
            return redirect(url_for("admin.tag_add"))
        new_tag = Tag(
            name=data["name"]
        )
        db.session.add(new_tag)
        db.session.commit()
        flash("操作成功", "ok")
        return redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)


# 编辑标签
@admin.route("/tag_edit", methods=["GET", "POST"])
@admin_login_req
def tag_edit():
    tag_id = int(request.args.get("id"))
    tag = Tag.query.get_or_404(tag_id)
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        cnt = Tag.query.filter_by(name=data["name"]).count()
        if tag.name != data["name"] and cnt >= 1:
            flash("已存在！", "err")
            return redirect(url_for("admin.tag_edit", id=tag_id))
        tag.name = data["name"]
        db.session.add(tag)
        db.session.commit()
        flash("操作成功", "ok")
        return redirect(url_for("admin.tag_edit", id=tag_id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


# 标签列表（路由默认处理GET请求）
@admin.route("/tag_list")
@admin_login_req
def tag_list():
    page = int(request.args.get("page", "1"))
    size = int(request.args.get("size", "10"))
    page_data = Tag.query.order_by(
        Tag.create_time.desc()
    ).paginate(page=page, per_page=size)
    return render_template("admin/tag_list.html", page_data=page_data)


# 测试ajax交互
@admin.route("/test_ajax", methods=["GET", "POST"])
@admin_login_req
def test_ajax():
    form = request.form
    print(form)
    name = form.get("name")
    age = form.get("age")
    gender = form.get("gender")
    print(name, age, gender)
    json_resp = {"code": 200, "msg": "Ajax Success!", "data": None}
    return jsonify(json_resp)


# 删除标签
@admin.route("/tag_del", methods=["GET", "POST"])
@admin_login_req
def tag_del():
    try:
        form = request.form
        id = int(form.get("id"))
        tag = Tag.query.filter_by(id=id).first_or_404()
        db.session.delete(tag)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify(ResultEnum.obj2json(ResultEnum.FAIL.value))
    return jsonify(ResultEnum.obj2json(ResultEnum.SUCCESS.value))


@admin.route("/video_add/", methods=["GET", "POST"])
@admin_login_req
def video_add():
    return render_template("admin/video_add.html")


@admin.route("/video_list/", methods=["GET", "POST"])
@admin_login_req
def video_list():
    return render_template("admin/video_list.html")


@admin.route("/preview_add/", methods=["GET", "POST"])
@admin_login_req
def preview_add():
    return render_template("admin/preview_add.html")


@admin.route("/preview_list/", methods=["GET", "POST"])
@admin_login_req
def preview_list():
    return render_template("admin/preview_list.html")


@admin.route("/user_list/", methods=["GET", "POST"])
@admin_login_req
def user_list():
    return render_template("admin/user_list.html")


@admin.route("/user_view/", methods=["GET", "POST"])
@admin_login_req
def user_view():
    return render_template("admin/user_view.html")


@admin.route("/comment_list/", methods=["GET", "POST"])
@admin_login_req
def comment_list():
    return render_template("admin/comment_list.html")


@admin.route("/collection_list/", methods=["GET", "POST"])
@admin_login_req
def collection_list():
    return render_template("admin/collection_list.html")


@admin.route("/admin_op_log_list/", methods=["GET", "POST"])
@admin_login_req
def admin_op_log_list():
    return render_template("admin/admin_op_log_list.html")


@admin.route("/admin_login_log_list/", methods=["GET", "POST"])
@admin_login_req
def admin_login_log_list():
    return render_template("admin/admin_login_log_list.html")


@admin.route("/login_log_list/", methods=["GET", "POST"])
@admin_login_req
def login_log_list():
    return render_template("admin/login_log_list.html")


@admin.route("/auth_add/", methods=["GET", "POST"])
@admin_login_req
def auth_add():
    return render_template("admin/auth_add.html")


@admin.route("/auth_list/", methods=["GET", "POST"])
@admin_login_req
def auth_list():
    return render_template("admin/auth_list.html")


@admin.route("/role_add/", methods=["GET", "POST"])
@admin_login_req
def role_add():
    return render_template("admin/role_add.html")


@admin.route("/role_list/", methods=["GET", "POST"])
@admin_login_req
def role_list():
    return render_template("admin/role_list.html")


@admin.route("/admin_user_add/", methods=["GET", "POST"])
@admin_login_req
def admin_user_add():
    return render_template("admin/admin_user_add.html")


@admin.route("/admin_user_list/", methods=["GET", "POST"])
@admin_login_req
def admin_user_list():
    return render_template("admin/admin_user_list.html")





