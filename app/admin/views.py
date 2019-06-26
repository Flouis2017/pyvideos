# coding:utf8
from . import admin
from flask import render_template, redirect, url_for, flash, session, request, jsonify
from app.admin.forms import *
from app.models import *
from functools import wraps
from app import db, app
from app.admin.result import ResultEnum
from app.common.util import SqlUtil
from werkzeug.utils import secure_filename
import os
import uuid
import datetime


# 登录拦截器(注意装饰器的写法)
def admin_login_req(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorator


# 修改文件名称
def change_filename(filename):
    file_info = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + file_info[-1]
    return filename


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
def test_ajax():
    form = request.form
    name = form.get("name")
    age = form.get("age")
    gender = form.get("gender")
    print(name, age, gender)
    sql = "SELECT au.id AS user_id, au.username AS username, r.name AS role_name, r.auth_set AS auth_set" \
          " FROM admin_user au INNER JOIN role r ON au.role_id = r.id where au.id = :user_id"

    return jsonify(SqlUtil.exe_sql(sql, {"user_id": 1}))


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


# 添加视频
@admin.route("/video_add/", methods=["GET", "POST"])
@admin_login_req
def video_add():
    form = VideoForm()
    if form.validate_on_submit():
        try:
            data = form.data
            file_url = secure_filename(form.url.data.filename)
            file_logo = secure_filename(form.logo.data.filename)
            up_dir_path = app.config["UP_DIR"]
            if not os.path.exists(up_dir_path):
                os.makedirs(up_dir_path)
                # os.chmod(up_dir_path, "rw")
            url = change_filename(file_url)
            logo = change_filename(file_logo)

            # 保存文件
            form.url.data.save(up_dir_path + "/" + url)
            form.logo.data.save(up_dir_path + "/" + logo)

            video = Video(
                title=data["title"],
                url=url,
                info=data["info"],
                logo=logo,
                star=data["star"],
                play_amount=0,
                comment_amount=0,
                tag_id=data["tag_id"],
                area=data["area"],
                release_time=data["release_time"],
                length=data["length"]
            )
            db.session.add(video)
            db.session.commit()
            flash("添加视频成功！", "ok")
        except Exception as e:
            print(e)
            flash("服务器异常，添加视频失败！", "err")

        return redirect(url_for("admin.video_add"))

    return render_template("admin/video_add.html", form=form)


# 视频列表
@admin.route("/video_list/", methods=["GET", "POST"])
@admin_login_req
def video_list():
    return render_template("admin/video_list.html")


# 添加预告
@admin.route("/preview_add/", methods=["GET", "POST"])
@admin_login_req
def preview_add():
    return render_template("admin/preview_add.html")


# 预告列表
@admin.route("/preview_list/", methods=["GET", "POST"])
@admin_login_req
def preview_list():
    return render_template("admin/preview_list.html")


# 用户列表
@admin.route("/user_list/", methods=["GET", "POST"])
@admin_login_req
def user_list():
    return render_template("admin/user_list.html")


# 用户查看
@admin.route("/user_view/", methods=["GET", "POST"])
@admin_login_req
def user_view():
    return render_template("admin/user_view.html")


# 评论列表
@admin.route("/comment_list/", methods=["GET", "POST"])
@admin_login_req
def comment_list():
    return render_template("admin/comment_list.html")


# 收藏列表
@admin.route("/collection_list/", methods=["GET", "POST"])
@admin_login_req
def collection_list():
    return render_template("admin/collection_list.html")


# 后台操作记录列表
@admin.route("/admin_op_log_list/", methods=["GET", "POST"])
@admin_login_req
def admin_op_log_list():
    return render_template("admin/admin_op_log_list.html")


# 后台登录记录列表
@admin.route("/admin_login_log_list/", methods=["GET", "POST"])
@admin_login_req
def admin_login_log_list():
    return render_template("admin/admin_login_log_list.html")


# 客户端登录记录列表
@admin.route("/login_log_list/", methods=["GET", "POST"])
@admin_login_req
def login_log_list():
    return render_template("admin/login_log_list.html")


# 添加权限
@admin.route("/auth_add/", methods=["GET", "POST"])
@admin_login_req
def auth_add():
    return render_template("admin/auth_add.html")


# 权限列表
@admin.route("/auth_list/", methods=["GET", "POST"])
@admin_login_req
def auth_list():
    return render_template("admin/auth_list.html")


# 添加角色
@admin.route("/role_add/", methods=["GET", "POST"])
@admin_login_req
def role_add():
    return render_template("admin/role_add.html")


# 角色列表
@admin.route("/role_list/", methods=["GET", "POST"])
@admin_login_req
def role_list():
    return render_template("admin/role_list.html")


# 添加管理员
@admin.route("/admin_user_add/", methods=["GET", "POST"])
@admin_login_req
def admin_user_add():
    return render_template("admin/admin_user_add.html")


# 管理员列表
@admin.route("/admin_user_list/", methods=["GET", "POST"])
@admin_login_req
def admin_user_list():
    return render_template("admin/admin_user_list.html")





