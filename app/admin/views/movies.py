# -*- coding:utf-8 -*-
# @Time : 3/24/19 9:42 AM
# @Author : westos-dd
# @Filename : movies.py
# @Software : PyCharm
"""

"""
import os

from werkzeug.utils import secure_filename

from app import app, db
from app.admin import admin
from app.admin.forms.movies import MovieForm
from app.admin.utils import is_admin_login, writer_adminOpLog
from app.home import change_file
from app.models import Movie
from flask import render_template, redirect, url_for, flash


@admin.route('/movie/list/')
@admin.route('/movie/list/<int:page>/')
def movie_list(page=1):
    moviesPageObj=Movie.query.paginate(page=page,per_page=app.config['PER_PAGE'])
    return render_template('admin/movies/list.html',moviesPageObj=moviesPageObj)



@admin.route('/movie/add/',methods=['GET','POST'])
def movie_add():
    form=MovieForm()
    if form.validate_on_submit():
        url=form.url.data.filename
        logo=form.logo.data.filename

        file_save_path=app.config['MOVIE_DIR']
        if not os.path.exists(file_save_path):
            os.makedirs(file_save_path)
        url=change_file(url)
        logo=change_file(logo)
        form.url.data.save(os.path.join(file_save_path,url))
        form.logo.data.save(os.path.join(file_save_path,logo))
        movie=Movie(
            name=form.name.data,
            info=form.info.data,
            star=form.star.data,
            area=form.area.data,
            length=form.length.data,
            create_time=form.release_time,
            url=url,
            logo=logo,
            tag_id=form.tag_id.data
        )
        db.session.add(movie)
        db.session.commit()
        flash('添加电影成功')

        writer_adminOpLog('删除电影%s成功！' % (movie.name))

        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movies/add.html',form=form)



@admin.route('/movie/edit/<int:id>/', methods=['GET', 'POST'])
@is_admin_login

def movie_edit(id):
    movie = Movie.query.get_or_404(id)
    # 给表单赋初始值，文件表单不处理
    form = MovieForm(
        name=movie.name,
        # url=movie.url,  # 上传文件，这样赋初始值无效，在前端可以通过上传路径+movie.url来获取文件的保存路径，显示在页面上
        info=movie.info,
        # logo=movie.logo,  # 上传图片和文件类似
        star=movie.star,
        tag_id=movie.tag_id,
        area=movie.area,
        create_time=movie.release_time,
        length=movie.length,
    )
    # 对于修改数据，电影文件和封面图已存在，可以非必填:
    # 按照教程上测试了validators参数，但始终不行，
    # 最终修改required的值就可以了
    form.url.validators = []
    form.logo.validators = []  # 验证列表为空

    if form.validate_on_submit():
        data = form.data
        # 提交的片名在数据库中已存在，且不是当前的电影名称
        if Movie.query.filter_by(name=data['name']).count() == 1 and movie.name != data['name']:
            flash('电影片名已存在，请检查', category='err')
            return redirect(url_for('admin.movie_edit', edit_id=id))
        # 以下和直接修改的数据
        movie.name = data['name']
        movie.info = data['info']
        movie.star = data['star']
        movie.tag_id = data['tag_id']
        movie.area = data['area']
        movie.release_time = data['release_time']
        movie.length = data['length']

        # 文件保存路径操作
        file_save_path = app.config['MOVIE_UP_DIR']  # 文件上传保存路径
        if not os.path.exists(file_save_path):
            os.makedirs(file_save_path)  # 如果文件保存路径不存在，则创建一个多级目录

        # 处理电影文件逻辑：先从磁盘中删除旧文件，然后保存新文件
        if form.url.data:  # 上传文件不为空，才进行保存
            # 删除以前的文件
            if os.path.exists(os.path.join(file_save_path, movie.url)):
                os.remove(os.path.join(file_save_path, movie.url))
            # 获取上传文件的名称
            file_url = secure_filename(form.url.data.filename)
            # 对上传的文件进行重命名
            movie.url = change_file(file_url)
            # 保存文件，需要给文件的保存路径+文件名
            form.url.data.save(file_save_path + movie.url)

        # 处理封面图
        if form.logo.data:
            if os.path.exists(os.path.join(file_save_path, movie.logo)):
                os.remove(os.path.join(file_save_path, movie.logo))
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_file(file_logo)
            form.logo.data.save(file_save_path + movie.logo)

        # 保存到数据库中;
        db.session.add(movie)
        db.session.commit()
        flash('修改电影%s成功' % (movie.name), 'ok')
        writer_adminOpLog('修改电影%s成功' % (movie.name))
        return redirect(url_for('admin.movie_edit', id=id))
    return render_template('admin/movies/edit.html',
                           form=form,
                           movie=movie)


@admin.route('/movie/delete/<int:id>/')
@is_admin_login

def movie_del(id=None):
    if id:
        movie = Movie.query.filter_by(id=id).first_or_404()
        # 删除电影同时要从磁盘中删除电影的文件和封面文件
        file_save_path = app.config['MOVIE_UP_DIR']  # 文件上传保存路径
        # 如果存在将进行删除，不判断，如果文件不存在,删除会报错
        if os.path.exists(os.path.join(file_save_path, movie.url)):
            os.remove(os.path.join(file_save_path, movie.url))
        if os.path.exists(os.path.join(file_save_path, movie.logo)):
            os.remove(os.path.join(file_save_path, movie.logo))

        # 删除数据库，提交修改，注意后面要把与电影有关的评论都要删除
        db.session.delete(movie)
        db.session.commit()
        # 删除后闪现消息
        flash('删除电影%s成功！' % (movie.name), category='ok')
        writer_adminOpLog('删除电影%s成功！' % (movie.name))
    return redirect(url_for('admin.movie_list', page=1))