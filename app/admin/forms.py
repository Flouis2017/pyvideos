# coding : utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


# 管理员登录(验证)表单
class LoginForm(FlaskForm):
    account = StringField(

    )

