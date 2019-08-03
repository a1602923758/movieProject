# -*- coding:utf-8 -*-
# @Time : 3/24/19 9:51 AM
# @Author : westos-dd
# @Filename : utils.py
# @Software : PyCharm
"""

"""
from functools import wraps

from flask import session, flash, redirect, url_for, request

from app import db
from app.models import AdminOpLog


def is_admin_login(f):
    """用来判断用户是否登录成功"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        # 判断session对象中是否有seesion['user'],
        # 如果包含信息， 则登录成功， 可以访问主页；
        # 如果不包含信息， 则未登录成功， 跳转到登录界面;；
        if session.get('admin', None):
            return f(*args, **kwargs)
        else:
            flash("用户必须登录才能访问%s" % (f.__name__))
            return redirect(url_for('admin.login'))

    return wrapper



def writer_adminOpLog(info):
    admin_id=session.get('admin_id',None)
    ip=request.remote_addr
    admin_op_log=AdminOpLog(reason=info,admin_id=admin_id,ip=ip)
    db.session.add(admin_op_log)
    db.session.commit()