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


# 上下文处理器 —— 封装全局变量
@admin.context_processor
def tpl_extra():
    data = dict(
        online_date = datetime.datetime.now().strftime("%Y-%m-%d")
    )
    return data


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


# 删除文件
def del_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


# 记录管理员操作日志
def record_admin_op_log(detail):
    admin_op_log = AdminOpLog(
        admin_user_id=session["admin_user_id"],
        ip=request.remote_addr,
        detail=detail
    )
    db.session.add(admin_op_log)
    db.session.commit()


# 记录管理员登录日志
def record_admin_login_log():
    admin_login_log = AdminLoginLog(
        admin_user_id=session["admin_user_id"],
        ip=request.remote_addr
    )
    db.session.add(admin_login_log)
    db.session.commit()


@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")


# 登录
@admin.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        username = data["username"]
        admin_user = AdminUser.query.filter_by(username=username).first()
        if not admin_user.check_pwd(data["pwd"]):
            flash("密码错误！")
            return redirect(url_for("admin.login"))
        session["username"] = username
        session["admin_user_id"] = admin_user.id

        # 登录记录
        record_admin_login_log()

        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


# 退出
@admin.route("/logout", methods=["GET", "POST"])
@admin_login_req
def logout():
    session.pop("username", None)
    session.pop("admin_user_id", None)
    return redirect(url_for("admin.login"))


# 修改密码页面跳转
@admin.route("/pwd", methods=["GET", "POST"])
@admin_login_req
def pwd():
    return render_template("admin/pwd.html")


# 修改密码
@admin.route("/modify_pwd", methods=["GET", "POST"])
@admin_login_req
def modify_pwd():
    try:
        newpwd = request.form.get("newpwd")
        # 获取当前管理员用户
        admin_user = AdminUser.query.filter_by(id=session["admin_user_id"]).first()
        # 更新密码
        from werkzeug.security import generate_password_hash
        admin_user.pwd = generate_password_hash(newpwd)
        db.session.add(admin_user)
        db.session.commit()

        # 修改密码日志记录
        record_admin_op_log("修改密码")
    except Exception as e:
        print(e)
        ResultEnum.FAIL.value.msg = "服务器异常，修改失败"
        return jsonify(ResultEnum.obj2json(ResultEnum.FAIL.value))
    ResultEnum.SUCCESS.value.msg = "修改成功"
    return jsonify(ResultEnum.obj2json(ResultEnum.SUCCESS.value))


# 添加标签
@admin.route("/tag_add", methods=["GET", "POST"])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        tag_name = form.data["name"]
        cnt = Tag.query.filter_by(name=tag_name).count()
        if cnt >= 1:
            flash("已存在！", "err")
            return redirect(url_for("admin.tag_add"))
        new_tag = Tag(
            name=tag_name
        )
        db.session.add(new_tag)
        db.session.commit()
        flash("操作成功", "ok")
        record_admin_op_log("添加标签 " + tag_name)
        return redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)


# 编辑标签
@admin.route("/tag_edit", methods=["GET", "POST"])
@admin_login_req
def tag_edit():
    id = int(request.args.get("id"))
    tag = Tag.query.get_or_404(id)
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        cnt = Tag.query.filter_by(name=data["name"]).count()
        if tag.name != data["name"] and cnt >= 1:
            flash("已存在！", "err")
            return redirect(url_for("admin.tag_edit", id=id))
        tag.name = data["name"]
        db.session.add(tag)
        db.session.commit()
        flash("操作成功", "ok")
        record_admin_op_log("编辑标签(id: " + str(id) + ")")
        return redirect(url_for("admin.tag_edit", id=id))
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
    # print(page_data)
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
        tag_id = int(request.form.get("id"))
        tag = Tag.query.filter_by(id=tag_id).first_or_404()
        tag_name = tag.name
        db.session.delete(tag)
        db.session.commit()
        record_admin_op_log("删除标签 " + tag_name)
    except Exception as e:
        print(e)
        ResultEnum.FAIL.value.msg = "服务器异常，删除失败"
        return jsonify(ResultEnum.obj2json(ResultEnum.FAIL.value))
    ResultEnum.SUCCESS.value.msg = "删除成功"
    return jsonify(ResultEnum.obj2json(ResultEnum.SUCCESS.value))


# 添加视频
@admin.route("/video_add", methods=["GET", "POST"])
@admin_login_req
def video_add():
    form = VideoForm()
    if form.validate_on_submit():
        try:
            data = form.data

            # 视频标题不允许重复添加
            cnt = Video.query.filter_by(title=data["title"]).count()
            if cnt >= 1:
                flash("视频标题已存在！", "err")
                return redirect(url_for("admin.video_add"))

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
            flash("添加成功！", "ok")
        except Exception as e:
            print(e)
            flash("服务器异常，添加失败！", "err")

        return redirect(url_for("admin.video_add"))

    return render_template("admin/video_add.html", form=form)


# 视频列表
@admin.route("/video_list", methods=["GET", "POST"])
@admin_login_req
def video_list():
    page = int(request.args.get("page", "1"))
    size = int(request.args.get("size", "10"))
    page_data = db.session.query(Video.id, Video.title, Video.length, Tag.name, Video.area,  Video.star,
                                 Video.play_amount, Video.comment_amount, Video.release_time) \
        .join(Tag, Tag.id == Video.tag_id).filter() \
        .order_by(Video.create_time.desc()).paginate(page=page, per_page=size)
    # page_data = Video.query.join(Tag, Tag.id == Video.tag_id).filter()\
    #     .order_by(Video.create_time.desc()).paginate(page=page, per_page=size)
    return render_template("admin/video_list.html", page_data=page_data, col_num=9)


# 删除视频
@admin.route("/video_del", methods=["GET", "POST"])
@admin_login_req
def video_del():
    try:
        video_id = int(request.form.get("id"))
        video = Video.query.filter_by(id=video_id).first_or_404()
        db.session.delete(video)
        db.session.commit()
        # TODO 实际上还需要删除视频相关的评论和相应的文件（视频源和封面图片）
        up_dir_path = app.config["UP_DIR"]
        del_file(up_dir_path + "/" + video.url)
        del_file(up_dir_path + "/" + video.logo)
    except Exception as e:
        print(e)
        ResultEnum.FAIL.value.msg = "服务器异常，删除失败"
        return jsonify(ResultEnum.obj2json(ResultEnum.FAIL.value))
    ResultEnum.SUCCESS.value.msg = "删除成功"
    return jsonify(ResultEnum.obj2json(ResultEnum.SUCCESS.value))


# 添加视频
@admin.route("/video_edit", methods=["GET", "POST"])
@admin_login_req
def video_edit():
    id = int(request.args.get("id"))
    video = Video.query.get_or_404(id)
    form = VideoForm()
    form.url.validators = []
    form.logo.validators = []
    if request.method == "GET":
        form.info.data = video.info
        form.tag_id.data = video.tag_id
        form.star.data = video.star
    if form.validate_on_submit():
        try:
            data = form.data
            # 去重处理：
            title = data["title"]
            video_cnt = Video.query.filter_by(title=title).count()
            if video_cnt >= 1 and video.title != title:
                flash("片名已存在！", "err")
                return redirect(url_for("admin.video_edit", id=video.id))

            # 修改数据：
            up_dir_path = app.config["UP_DIR"]
            if not os.path.exists(up_dir_path):
                os.makedirs(up_dir_path)
            if form.url.data.filename != "":
                # 先将原先的文件删除：
                del_file(up_dir_path+"/"+video.url)
                # 保存新文件
                file_url = secure_filename(form.url.data.filename)
                video.url = change_filename(file_url)
                form.url.data.save(up_dir_path + "/" + video.url)
            if form.logo.data.filename != "":
                del_file(up_dir_path+"/"+video.logo)
                file_logo = secure_filename(form.logo.data.filename)
                video.logo = change_filename(file_logo)
                form.logo.data.save(up_dir_path + "/" + video.logo)

            video.star = data["star"]
            video.tag_id = data["tag_id"]
            video.info = data["info"]
            video.title = title
            video.area = data["area"]
            video.length = data["length"]
            video.release_time = data["release_time"]
            db.session.add(video)
            db.session.commit()
            flash("编辑成功！", "ok")
        except Exception as e:
            print(e)
            flash("服务器异常，编辑失败！", "err")

        return redirect(url_for("admin.video_edit", id=video.id))

    return render_template("admin/video_edit.html", form=form, video=video)


# 添加预告
@admin.route("/preview_add", methods=["GET", "POST"])
@admin_login_req
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        try:
            data = form.data

            # 预告标题不允许重复添加
            title = data["title"]
            cnt = Preview.query.filter_by(title=title).count()
            if cnt >= 1:
                flash("预告标题已存在！", "err")
                return redirect(url_for("admin.preview_add"))

            # 保存logo图片：
            logo_file_name = secure_filename(form.logo.data.filename)
            up_dir_path = app.config["UP_DIR"]
            if not os.path.exists(up_dir_path):
                os.makedirs(up_dir_path)
            new_logo_file_name = change_filename(logo_file_name)
            form.logo.data.save(up_dir_path + "/" + new_logo_file_name)

            # 数据库落地
            preview = Preview(
                title=title,
                logo=new_logo_file_name
            )
            db.session.add(preview)
            db.session.commit()
            flash("添加预告成功", "ok")
        except Exception as e:
            print(e)
            flash("服务器异常，添加预告失败！", "err")

        return redirect(url_for("admin.preview_add"))

    return render_template("admin/preview_add.html", form=form)


# 预告列表
@admin.route("/preview_list", methods=["GET", "POST"])
@admin_login_req
def preview_list():
    page = int(request.args.get("page", "1"))
    size = int(request.args.get("size", "10"))
    page_data = db.session.query(Preview.id, Preview.title, Preview.logo, Preview.create_time) \
                  .order_by(Preview.create_time.desc()).paginate(page=page, per_page=size)
    return render_template("admin/preview_list.html", page_data=page_data, col_num=4)


# 删除预告
@admin.route("/preview_del", methods=["GET", "POST"])
@admin_login_req
def preview_del():
    try:
        preview_id = int(request.form.get("id"))
        preview = Preview.query.filter_by(id=preview_id).first_or_404()

        # 将对应的预告封面(logo)文件删除
        del_file(app.config["UP_DIR"] + "/" + preview.logo)
        # 数据库相应记录删除
        db.session.delete(preview)
        db.session.commit()
    except Exception as e:
        print(e)
        ResultEnum.FAIL.value.msg = "服务器异常，删除失败"
        return jsonify(ResultEnum.obj2json(ResultEnum.FAIL.value))
    ResultEnum.SUCCESS.value.msg = "删除成功"
    return jsonify(ResultEnum.obj2json(ResultEnum.SUCCESS.value))


# 添加预告
@admin.route("/preview_edit", methods=["GET", "POST"])
@admin_login_req
def preview_edit():
    id = int(request.args.get("id"))
    preview = Preview.query.get_or_404(id)
    form = PreviewForm()
    form.logo.validators = []   # 去掉封面为空校验
    if form.validate_on_submit():
        try:
            data = form.data
            # 去重处理：
            title = data["title"]
            cnt = Preview.query.filter_by(title=title).count()
            if cnt >= 1 and preview.title != title:
                flash("预告标题已存在！", "err")
                return redirect(url_for("admin.preview_edit", id=preview.id))

            # 更新logo图片：
            up_dir_path = app.config["UP_DIR"]
            if not os.path.exists(up_dir_path):
                os.makedirs(up_dir_path)
            if form.logo.data.filename != "":
                del_file(up_dir_path + "/" + preview.logo)
                logo_filename = secure_filename(form.logo.data.filename)
                preview.logo = change_filename(logo_filename)
                form.logo.data.save(up_dir_path + "/" + preview.logo)

            # 更新数据：
            preview.title = title
            db.session.add(preview)
            db.session.commit()
            flash("编辑成功", "ok")

        except Exception as e:
            print(e)
            flash("服务器异常，编辑预告失败！", "err")

        return redirect(url_for("admin.preview_edit", id=preview.id))

    return render_template("admin/preview_edit.html", form=form, preview=preview)


# 用户列表
@admin.route("/user_list", methods=["GET", "POST"])
@admin_login_req
def user_list():
    page = int(request.args.get("page", "1"))
    per_page = int(request.args.get("size", "10"))
    page_data = db.session.query(User.id, User.username, User.email, User.phone, User.avatar, User.create_time) \
        .order_by(User.id.desc()).paginate(page=page, per_page=per_page)

    return render_template("admin/user_list.html", page_data=page_data, col_num=6)


# 用户查看
@admin.route("/user_view", methods=["GET", "POST"])
@admin_login_req
def user_view():
    user_id = request.args.get("user_id")
    user = User.query.get_or_404(user_id)
    return render_template("admin/user_view.html", user=user)


# 评论列表
@admin.route("/comment_list", methods=["GET", "POST"])
@admin_login_req
def comment_list():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("size", 10))
    page_data = db.session.query(Comment.id, User.avatar, User.username, Comment.create_time, Video.title, Comment.content) \
        .join(User, Comment.user_id == User.id).join(Video, Comment.video_id == Video.id).filter() \
        .order_by(Comment.id.desc()).paginate(page=page, per_page=per_page)
    return render_template("admin/comment_list.html", page_date=page_data)


# 收藏列表
@admin.route("/collection_list", methods=["GET", "POST"])
@admin_login_req
def collection_list():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    page_date = db.session.query(Collection.id, Video.title, User.username, Collection.create_time)\
        .join(Video, Collection.video_id == Video.id).join(User, Collection.user_id == User.id).filter()\
        .order_by(Collection.id.desc()).paginate(page=page, per_page=per_page)
    return render_template("admin/collection_list.html", page_date=page_date, col_num=4)


# 后台操作记录列表
@admin.route("/admin_op_log_list", methods=["GET", "POST"])
@admin_login_req
def admin_op_log_list():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    page_data = db.session.query(AdminOpLog.id, AdminUser.username, AdminOpLog.create_time, AdminOpLog.detail, AdminOpLog.ip)\
        .join(AdminUser, AdminOpLog.admin_user_id == AdminUser.id).filter()\
        .order_by(AdminOpLog.id.desc()).paginate(page=page, per_page=size)
    return render_template("admin/admin_op_log_list.html", page_data=page_data, col_num=5)


# 后台登录记录列表
@admin.route("/admin_login_log_list", methods=["GET", "POST"])
@admin_login_req
def admin_login_log_list():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    page_data = db.session.query(AdminLoginLog.id, AdminUser.username, AdminLoginLog.create_time, AdminLoginLog.ip)\
        .join(AdminUser, AdminUser.id == AdminLoginLog.admin_user_id).filter()\
        .order_by(AdminLoginLog.id.desc()).paginate(page=page, per_page=size)
    return render_template("admin/admin_login_log_list.html", page_data=page_data, col_num=4)


# 客户端登录记录列表
@admin.route("/login_log_list", methods=["GET", "POST"])
@admin_login_req
def login_log_list():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    page_data = db.session.query(LoginLog.id, User.username, LoginLog.create_time, LoginLog.ip)\
        .join(User, LoginLog.user_id == User.id).filter()\
        .order_by(LoginLog.id.desc()).paginate(page=page, per_page=size)
    return render_template("admin/login_log_list.html", page_data=page_data, col_num=4)


# 添加权限
@admin.route("/auth_add", methods=["GET", "POST"])
@admin_login_req
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        try:
            data = form.data

            # 去重处理
            name = data["name"]
            cnt = Auth.query.filter_by(name=name).count()
            if cnt >= 1:
                flash("权限已存在！", "err")
                return redirect(url_for("admin.auth_add"))

            # 保存权限(数据库落地)
            auth = Auth(
                name=name,
                url=data["url"]
            )
            db.session.add(auth)
            db.session.commit()
            flash("添加权限成功", "ok")
        except Exception as e:
            print(e)
            flash("服务器异常，添加权限失败！", "err")
        return redirect(url_for("admin.auth_add"))
    return render_template("admin/auth_add.html", form=form)


# 权限列表
@admin.route("/auth_list", methods=["GET", "POST"])
@admin_login_req
def auth_list():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    page_data = db.session.query(Auth.id, Auth.name, Auth.url, Auth.create_time)\
        .join().filter().order_by().paginate(page=page, per_page=size)
    return render_template("admin/auth_list.html", page_data=page_data, col_num=4)


# 编辑权限
@admin.route("/auth_edit", methods=["GET", "POST"])
@admin_login_req
def auth_edit():
    id = int(request.args.get("id"))
    auth = Auth.query.get_or_404(id)
    form = AuthForm()
    if form.validate_on_submit():
        try:
            data = form.data

            # 去重处理
            name = data["name"]
            cnt = Auth.query.filter_by(name=name).count()
            if cnt >= 1 and auth.name != name:
                flash("权限已存在！", "err")
                return redirect(url_for("admin.auth_edit", id=auth.id))

            # 更新数据
            auth.name = name
            auth.url = data["url"]
            db.session.add(auth)
            db.session.commit()
            flash("编辑成功", "ok")
        except Exception as e:
            print(e)
            flash("服务器异常，编辑失败！", "err")
        return redirect(url_for("admin.auth_edit", id=auth.id))
    return render_template("admin/auth_edit.html", form=form, auth=auth)


# 删除权限
@admin.route("/auth_del", methods=["GET", "POST"])
@admin_login_req
def auth_del():
    try:
        auth_id = int(request.form.get("id"))
        auth = Auth.query.get_or_404(auth_id)
        db.session.delete(auth)
        db.session.commit()
    except Exception as e:
        print(e)
        ResultEnum.FAIL.value.msg = "服务器异常，删除失败！"
        return jsonify(ResultEnum.obj2json(ResultEnum.FAIL.value))
    ResultEnum.SUCCESS.value.msg = "删除成功"
    return jsonify(ResultEnum.obj2json(ResultEnum.SUCCESS.value))


# 添加角色
@admin.route("/role_add", methods=["GET", "POST"])
@admin_login_req
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        try:
            data = form.data
            # 去重处理
            name = data["name"]
            cnt = Role.query.filter_by(name=name).count()
            if cnt >= 1:
                flash("角色已存在！", "err")
                return redirect(url_for("admin.role_add"))

            # 数据库落地
            role = Role(
                name=name,
                auth_set=",".join(map(lambda v: str(v), data["auth_set"]))
            )
            db.session.add(role)
            db.session.commit()
            flash("添加角色成功", "ok")
        except Exception as e:
            print(e)
            flash("服务器异常，添加角色失败！", "err")
        return redirect(url_for("admin.role_add"))
    return render_template("admin/role_add.html", form=form)


# 角色列表
@admin.route("/role_list", methods=["GET", "POST"])
@admin_login_req
def role_list():
    return render_template("admin/role_list.html")


# 添加管理员
@admin.route("/admin_user_add", methods=["GET", "POST"])
@admin_login_req
def admin_user_add():
    return render_template("admin/admin_user_add.html")


# 管理员列表
@admin.route("/admin_user_list", methods=["GET", "POST"])
@admin_login_req
def admin_user_list():
    return render_template("admin/admin_user_list.html")





