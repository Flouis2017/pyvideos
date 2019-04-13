# coding : utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import AdminUser


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

