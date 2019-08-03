# -*- coding:utf-8 -*-
# @Time : 3/24/19 9:43 AM
# @Author : westos-dd
# @Filename : main.py
# @Software : PyCharm
"""

"""
from werkzeug.security import generate_password_hash

from app import db
from app.admin import admin
from flask import render_template, session, request, flash, redirect, url_for

from app.admin.forms.main import LoginForm, ChangePwd
from app.admin.utils import is_admin_login
from app.models import Admin,AdminLog


@admin.route('/')

def index():
    return render_template('admin/base.html')


@admin.route('/login/',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        name=form.username.data
        password=form.password.data
        admin=Admin.query.filter_by(name=name).first()
        if admin and admin.check(password):
            session['admin_id']=admin.id
            session['admin']=admin.name
            adminLog=AdminLog(admin_id=admin.id,ip=request.remote_addr,area='陕西西安')
            db.session.add(adminLog)
            db.session.commit()
            flash('管理员%s登录成功' %(name))
            return redirect(url_for('admin.index'))
        else:
            flash('管理员登录失败' )
            return redirect(url_for('admin.login'))
    else:
        return render_template('admin/login.html',form=form)


@admin.route('/logout/')
@is_admin_login
def logout():
    session.pop('admin_id', None)
    session.pop('admin', None)

    return redirect(url_for('admin.login'))

@admin.route('/pwd/',methods=['GET','POST'])
@is_admin_login
def pwd():
    form=ChangePwd()
    admin=Admin.query.filter_by(name=session.get('admin')).first()
    if form.validate_on_submit():
        oldPwd=request.form['old_pwd']
        newPwd=request.form['new_pwd']
        print(oldPwd)
        if not admin.check(oldPwd):
            flash('旧密码不正确')
            return redirect(url_for('admin.pwd'))
        admin.password=generate_password_hash(newPwd)
        db.session.add(admin)
        db.session.commit()
        flash('修改密码成功')
        return redirect(url_for('admin.pwd'))
    return render_template('admin/pwd.html',form=form)