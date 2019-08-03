# -*- coding:utf-8 -*-
# @Time : 3/24/19 9:41 AM
# @Author : westos-dd
# @Filename : tags.py
# @Software : PyCharm
"""

"""


from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


class BaseForm(FlaskForm):
    name=StringField(
        label='标签名称',
        validators=[
            DataRequired()
        ],
        render_kw={
            'placeholder':'添加新标签'
        }
    )


class TagForm(BaseForm):
    submit=SubmitField(
        label='添加标签'
    )


class EditTagForm(BaseForm):
    submit=SubmitField(
        label='编辑标签'
    )