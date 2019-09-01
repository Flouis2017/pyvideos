# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError
from app.models import User


class RegisterForm(FlaskForm):
	username = StringField(
		label="用户名",
		validators=[
			DataRequired("请输入用户名！")
		],
		description="用户名",
		render_kw={
			"class": "form-control input-lg"
		}
	)
	email = StringField(
		label="邮箱",
		validators=[
			DataRequired("请输入邮箱！"),
			Email("不合法的邮箱！")
		],
		description="邮箱",
		render_kw={
			"class": "form-control input-lg"
		}
	)
	phone = StringField(
		label="手机",
		validators=[
			DataRequired("请输入手机！"),
			Regexp("1[3458]\\d{9}", message="不合法的手机号码！")
		],
		description="手机",
		render_kw={
			"class": "form-control input-lg"
		}
	)
	pwd = PasswordField(
		label="密码",
		validators=[
			DataRequired("请输入密码")
		],
		render_kw={
			"class": "form-control input-lg"
		}
	)
	re_pwd = PasswordField(
		label="确认密码",
		validators=[
			DataRequired("请确认密码"),
			EqualTo("pwd", message="两次密码不一致！")
		],
		render_kw={
			"class": "form-control input-lg"
		}
	)
	submit = SubmitField(
		"注册",
		render_kw={
			"class": "btn btn-lg btn-success btn-block"
		}
	)

	def validate_username(self, field):
		cnt = User.query.filter_by(username=field.data).count()
		if cnt >= 1:
			raise ValidationError("用户名已存在！")

	def validate_email(self, field):
		cnt = User.query.filter_by(email=field.data).count()
		if cnt >= 1:
			raise ValidationError("邮箱已使用！")

	def validate_phone(self, field):
		cnt = User.query.filter_by(phone=field.data).count()
		if cnt >= 1:
			raise ValidationError("手机已绑定！")


class LoginForm(FlaskForm):
	account = StringField(
		label="账号",
		validators=[
			DataRequired("请输入用户名/邮箱/手机号码")
		],
		description="账号",
		render_kw={
			"class": "form-control input-lg",
			"placeholder": "请输入用户名/邮箱/手机号码"
		}
	)
	pwd = PasswordField(
		label="密码",
		validators=[
			DataRequired("请输入密码")
		],
		render_kw={
			"class": "form-control input-lg",
			"placeholder": "请输入密码"
		}
	)
	submit = SubmitField(
		"登录",
		render_kw={
			"class": "btn btn-lg btn-success btn-block"
		}
	)


class UserDetailForm(FlaskForm):
	username = StringField(
		label="用户名",
		validators=[
			DataRequired("请输入用户名！")
		],
		description="用户名",
		render_kw={
			"class": "form-control",
			"readonly": "true"
		}
	)
	email = StringField(
		label="邮箱",
		validators=[
			DataRequired("请输入邮箱！"),
			Email("不合法的邮箱！")
		],
		description="邮箱",
		render_kw={
			"class": "form-control"
		}
	)
	phone = StringField(
		label="手机",
		validators=[
			DataRequired("请输入手机！"),
			Regexp("1[3458]\\d{9}", message="不合法的手机号码！")
		],
		description="手机",
		render_kw={
			"class": "form-control"
		}
	)
	avatar = FileField(
		label="头像",
		description="头像"
	)
	info = TextAreaField(
		label="简介",
		description="简介",
		render_kw={
			"class": "form-control",
			"rows": 10
		}
	)

	submit = SubmitField(
		"保存",
		render_kw={
			"class": "btn btn-success"
		}
	)


class PwdForm(FlaskForm):
	newpwd = PasswordField(
		label="新密码",
		validators=[
			DataRequired("请输入新密码")
		],
		render_kw={
			"class": "form-control"
		}
	)
	re_pwd = PasswordField(
		label="确认密码",
		validators=[
			DataRequired("请确认密码"),
			EqualTo("newpwd", message="两次密码不一致！")
		],
		render_kw={
			"class": "form-control"
		}
	)
	submit = SubmitField(
		"修改密码",
		render_kw={
			"class": "btn btn-success"
		}
	)

