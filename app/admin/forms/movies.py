# -*- coding:utf-8 -*-
# @Time : 3/24/19 9:41 AM
# @Author : westos-dd
# @Filename : movies.py
# @Software : PyCharm
"""

"""


from flask_wtf import FlaskForm
from wtforms import StringField,FileField,SelectField,TextAreaField,DateTimeField,SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

from app.models import Tag


class BaseForm(FlaskForm):

    def __init__(self,*args,**kwargs):
        super(BaseForm, self).__init__(*args,**kwargs)
        self.tag_id.choices=[(tag.id,tag.name) for tag in Tag.query.all()]

    name=StringField(
        '电影名称',
        validators=[
            DataRequired()
        ]
    )
    url=FileField(
        label='电影文件',
        validators=[
            DataRequired(),
            FileAllowed(['mp4','avi'],message='电影格式不正确')
        ]
    )
    info=TextAreaField(
        label='电影简介',
        validators=[
            DataRequired()
        ]
    )

    logo=FileField(
        '电影封面',
        validators=[
            DataRequired(),
            FileAllowed(['jpg','png'],message='封面格式不正确')
        ]
    )
    star=SelectField(
        label='电影星级',
        coerce=int,
        choices=[(i+1,'%s星' %(i+1)) for i in range(5)]
    )
    tag_id=SelectField(
        label='电影标签',
        coerce=int
    )
    area=StringField(
        '所在地区'
    )
    length=StringField(
        '播放时长'
    )
    release_time=StringField(
        '发行时间',
        validators=[

        ]
    )


class MovieForm(BaseForm):
    submit=SubmitField(
        label='添加'
    )

class EditMovieForm(BaseForm):
    submit=SubmitField(
        label='编辑'
    )