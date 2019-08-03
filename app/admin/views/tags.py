# -*- coding:utf-8 -*-
# @Time : 3/24/19 9:42 AM
# @Author : westos-dd
# @Filename : tags.py
# @Software : PyCharm
"""

"""
from app import app, db
from flask import render_template, redirect, flash, url_for, request
from app.admin import admin
from app.admin.forms.tags import TagForm, EditTagForm
from app.models import Tag


@admin.route('/tag/list/')
@admin.route('/tag/list/<int:page>/')
def list(page=1):
    tagsPageObj=Tag.query.paginate(page=page,per_page=app.config['PER_PAGE'])
    return render_template('admin/tag/list.html',tagsPageObj=tagsPageObj)


@admin.route('/tag/add/',methods=['GET','POST'])
def tag_add():
    form=TagForm()
    if form.validate_on_submit():
        name=form.name.data
        if Tag.query.filter_by(name=name).first():
            flash('标签已存在')
            return redirect(url_for('admin.tag_add'))
        tag=Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        flash('标签添加成功')
        return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag/add.html',form=form)

@admin.route('/tag/edit/<int:id>/',methods=['GET','POST'])
def tag_edit(id):
    tag=Tag.query.filter_by(id=id).first()
    form=EditTagForm()
    form.name.data=tag.name
    if form.validate_on_submit():
        name = request.form['name']
        if  Tag.query.filter_by(name=name).first() and tag.name!=name:
            flash('标签已存在')
            return redirect(url_for('admin.list'))
        tag.name=name
        db.session.add(tag)
        db.session.commit()
        flash('标签编辑成功')
        return redirect(url_for('admin.list'))
    return render_template('admin/tag/edit.html',form=form)

@admin.route('/tag/delete/<int:id>/')
def tag_del(id):
    tag=Tag.query.filter_by(id=id).first()
    db.session.delete(tag)
    db.session.commit()
    flash('标签删除成功')
    return redirect(url_for('admin.list'))
