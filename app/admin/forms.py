# coding : utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError
from app.models import AdminUser, Tag, Auth


# 视频表单中标签域需要
tags = Tag.query.all()

# 角色表单中权限集合域需要
auths = Auth.query.all()


# StringField对应的前端input元素type是text
# PasswordField对应的前端input元素type是password
# 管理员登录(验证)表单,定义完表单后，在前端使用{{ <属性名> }}这种方式去填充界面后，flask会帮我们做好表单验证
class LoginForm(FlaskForm):
    username = StringField(
        label="用户名",
        validators=[
            DataRequired("请输入用户名")
        ],
        description="用户名",
        render_kw={
            "class": "form-control",
            "placeholder": "用户名"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "密码"
        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_username(self, field):
        if AdminUser.query.filter_by(username=field.data).count() == 0:
            raise ValidationError("用户不存在！")


# 标签表单
class TagForm(FlaskForm):
    name = StringField(
        label="标签名称",
        validators=[
            DataRequired("请输入标签名称！")
        ],
        description="标签名称",
        render_kw={
            "class": "form-control",
            "id": "input_name"
        }
    )
    submit = SubmitField(
        "保存",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 视频表单
class VideoForm(FlaskForm):
    title = StringField(
        label="片名",
        validators=[
            DataRequired("请输入片名！")
        ],
        description="片名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片名！"
        }
    )
    url = FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件！")
        ],
        description="文件"
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介！")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 10
        }
    )
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="封面"
    )
    star = SelectField(
        label="星级",
        validators=[
            DataRequired("请选择星级！")
        ],
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description="星级",
        render_kw={
            "class": "form-control"
        }
    )
    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        description="标签",
        render_kw={
            "class": "form-control"
        }
    )
    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区！")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区！"
        }
    )
    length = StringField(
        label="片长",
        validators=[
            DataRequired("请输入片长！")
        ],
        description="片长",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片长！"
        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("请选择上映时间！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "id": "input_release_time",
            "placeholder": "请选择上映时间！"
        }
    )
    submit = SubmitField(
        "保存",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 预告表单
class PreviewForm(FlaskForm):
    title = StringField(
        label="预告标题",
        validators=[
            DataRequired("请输入预告标题！")
        ],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "id": "input_title"
        }
    )
    logo = FileField(
        label="预告封面",
        validators=[
            DataRequired("请上传预告封面！")
        ],
        description="预告封面"
    )
    submit = SubmitField(
        "保存",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 权限表单
class AuthForm(FlaskForm):
    name = StringField(
        label="权限名称",
        validators=[
            DataRequired("请输入权限名称！")
        ],
        description="权限名称",
        render_kw={
            "class": "form-control",
            "id": "input_name"
        }
    )
    url = StringField(
        label="权限路径",
        validators=[
            DataRequired("请输入权限路径！")
        ],
        description="权限路径",
        render_kw={
            "class": "form-control",
            "id": "input_url"
        }
    )
    submit = SubmitField(
        "保存",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 角色表单
class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("请输入角色名称！")
        ],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "id": "input_name"
        }
    )
    auth_set = SelectMultipleField(
        label="权限集合",
        validators=[
            DataRequired("至少需要选择一个权限！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in auths],
        description="权限集合",
        render_kw={
            "class": "form-control",
            "style": "height: 170px;"
        }
    )
    submit = SubmitField(
        "保存",
        render_kw={
            "class": "btn btn-primary"
        }
    )

