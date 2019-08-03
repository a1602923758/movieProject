# -*- coding:utf-8 -*-
# @Time : 3/24/19 9:42 AM
# @Author : westos-dd
# @Filename : main.py
# @Software : PyCharm
"""

"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class BaseForm(FlaskForm):
    username=StringField(
        label='用户名',
        validators=[
            DataRequired()
        ]
    )

    password=PasswordField(
        label='密码',
        validators=[
            DataRequired()
        ]
    )



class LoginForm(BaseForm):
    submit=SubmitField(
        label='登录'
    )



class ChangePwd(FlaskForm):
    old_pwd=PasswordField(
        label='旧密码',
        validators=[
            DataRequired()
        ],
        render_kw={
            'placeholder':'输入旧密码'
        }
    )

    new_pwd=PasswordField(
        label='新密码',
        validators=[
            DataRequired(),
        ],
        render_kw={
            'placeholder':'输入新密码'
        }
    )
    submit=SubmitField(
        label='修改密码'
    )