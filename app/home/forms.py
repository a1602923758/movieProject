from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField,PasswordField,SubmitField,FileField,TextAreaField,IntegerField
from wtforms.validators import DataRequired,Length,EqualTo,Email,Regexp




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
            DataRequired(),
            Length(6,12,message='密码格式不正确')
        ]
    )



class LoginForm(BaseForm):
    submit=SubmitField(
        label='登录'
    )

class RegisterForm(BaseForm):
    repassword=PasswordField(
        label='确认密码',
        validators=[
            EqualTo('password',message='确认密码与密码不一致')
        ]
    )
    email=StringField(
        label='邮箱地址',
        validators=[
            Email(message='邮箱格式不正确')
        ]
    )

    submit=SubmitField(
        label='注册'
    )


class UserForm(FlaskForm):
    username=StringField(
        label='用户名',
        validators=[
            DataRequired()
        ]
    )
    email=StringField(
        label='邮箱地址',
        validators=[
            Email(message='邮箱格式不正确')
        ]
    )
    phone=StringField(
        label='电话',
        validators=[
            Regexp(r'^1\d{10}$', message='电话号码格式不正确')
        ]
    )


    face=FileField(
        label='上传头像',
        validators=[
            FileAllowed(['jpg','png'],message='上传文件格式不正确')
        ]
    )
    info=TextAreaField(
        label='简介'
    )

    submit=SubmitField(
        label='更新信息'
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
            Length(6,16,message='密码长度不正确')
        ],
        render_kw={
            'placeholder':'输入新密码'
        }
    )
    submit=SubmitField(
        label='修改密码'
    )