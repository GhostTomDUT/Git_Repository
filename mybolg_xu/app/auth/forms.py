# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('记住我哎呦喂吼')
    submit = SubmitField('登录')

class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(),Length(1, 64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'只包含字母，数字，下划线和点号')])
    password2 = PasswordField('再输入一次密码', validators=[DataRequired(),EqualTo('password',message='密码需要一致')])
    submit = SubmitField('注册')

    def validate_email(self,field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('邮箱已经被注册了')
    def validate_username(self,field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('用户名已经被注册了')

class ChangePasswordForm(Form):
    password = PasswordField('旧密码', validators=[DataRequired()])
    password2 = PasswordField('新密码', validators=[DataRequired()])
    submit = SubmitField('登录')