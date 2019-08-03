import os

from app import db, app
from app.home import home
from flask import render_template, session, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash
from app.home.forms import LoginForm, RegisterForm, UserForm, ChangePwd
from app.home.utils import is_login, change_file
from app.models import User, UserLog, Comment, Subscript


@home.route('/')
def index():
    return render_template('home/base.html')

@home.route('/login/',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        u=User.query.filter_by(name=username).first()
        if u and u.check(password):
            session['user_id']=u.id
            session['user']=u.name
            userLog=UserLog(user_id=u.id,ip=request.remote_addr,area='陕西西安')
            db.session.add(userLog)
            db.session.commit()
            flash('用户%s登录成功' %(username))
            return redirect(url_for('home.user'))
        else:
            flash('用户登录失败')
            return redirect(url_for('home.login'))
    else:
        return render_template('home/login.html',form=form)


# 注册页面
@home.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 1. 从前端获取用户输入的值;
        email = form.email.data
        username = form.username.data
        password = form.password.data

        # 2. 判断用户是否已经存在? 如果返回位None，说明可以注册;
        u = User.query.filter_by(name=username).first()
        if u:
            flash("用户%s已经存在" % (u.name))
            return redirect(url_for('home.register'))
        else:
            u = User(name=username, email=email)
            u.password = generate_password_hash(password)
            db.session.add(u)
            db.session.commit()
            flash("注册用户%s成功" % (u.name))
            return redirect(url_for('home.login'))
    return render_template('home/register.html',
                           form=form)

@home.route('/logout/')
@is_login
def logout():
    session.pop('user_id', None)
    session.pop('user', None)

    return redirect(url_for('home.login'))


@home.route('/user/',methods=['GET','POST'])
@is_login
def user():
    form=UserForm()
    user=User.query.filter_by(name=session.get('user',None)).first()
    form.username.data=user.name
    form.email.data=user.email
    form.phone.data=user.phone
    form.info=user.info
    if form.validate_on_submit():
        username=request.form['username']
        email=request.form['email']
        face=form.face.data
        phone=request.form['phone']
        print(phone)
        info=request.form['info']
        if  User.query.filter_by(name=username).count() and username!=user.name:
            flash('更新失败，用户名已存在')
            return redirect(url_for('home.user'))
        if User.query.filter_by(email=email).count() and email!=user.email:
            flash('更新失败，邮箱已注册')
            return redirect(url_for('home.user'))

        if not os.path.exists(app.config['FC_DIR']):
            os.makedirs(app.config['FC_DIR'])
        if face:
            face_name=change_file(face.filename)
            if user.face and os.path.exists(os.path.join(app.config['FC_DIR'],user.face)):
                os.remove(os.path.join(app.config['FC_DIR'],user.face))
            form.face.data.save(os.path.join(app.config['FC_DIR'],face_name))
            user.face = face_name
        user.name=username
        user.email=email
        user.phone=phone
        user.info=info
        db.session.add(user)
        db.session.commit()
        flash('更新信息成功')
        return redirect(url_for('home.logout'))


    return render_template('home/user.html',form=form)

@home.route('/pwd/',methods=['GET','POST'])
@is_login
def pwd():
    form=ChangePwd()
    u=User.query.filter_by(name=session.get('user')).first()
    if form.validate_on_submit():
        oldPwd=request.form['old_pwd']
        newPwd=request.form['new_pwd']
        print(oldPwd)
        if not u.check(oldPwd):
            flash('旧密码不正确')
            return redirect(url_for('home.pwd'))
        u.password=generate_password_hash(newPwd)
        db.session.add(u)
        db.session.commit()
        flash('修改密码成功')
        return redirect(url_for('home.pwd'))
    return render_template('home/pwd.html',form=form)




@home.route('/comments/')
@home.route('/comments/<int:page>')
@is_login
def comments(page=1):
    comObj=Comment.query.filter_by(user_id=session.get('user_id')).paginate(page=page,per_page=app.config['PER_PAGE'])
    return render_template('home/comments.html',comObj=comObj)




@home.route('/userlog/')
@home.route('/userlog/<int:page>/')
@is_login
def userlog(page=1):
    uObj=UserLog.query.filter_by(user_id=session.get('user_id',None)).paginate(page=page,per_page=app.config['PER_PAGE'])
    return render_template('home/userlog.html',uObj=uObj)


@home.route('/moviecollect/<int:page>/')
@home.route('/moviecollect/')
@is_login
def moviecollect(page=1):
    movObj=Subscript.query.filter_by(user_id=session.get('user_id',None)).paginate(page=page,per_page=app.config['PER_PAGE'])
    return render_template('home/moviecollect.html',movObj=movObj)
