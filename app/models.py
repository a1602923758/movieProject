from app import db
from datetime import datetime
from werkzeug.security import check_password_hash

class Tag(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(20),unique=True)
    add_time=db.Column(db.DateTime,default=datetime.utcnow())
    movie=db.relationship('Movie',backref='tag')


    def __repr__(self):
        return '<Tag %s>' %(self.name)



class Movie(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(20),unique=True)
    add_time=db.Column(db.DateTime,default=datetime.utcnow())
    info=db.Column(db.Text)
    star=db.Column(db.SmallInteger)
    area=db.Column(db.String(20))
    length=db.Column(db.String(20))
    create_time=db.Column(db.DateTime)
    url=db.Column(db.String(200),unique=True)
    logo=db.Column(db.String(200),unique=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))


    comment=db.relationship('Comment',backref='movie')
    subscript=db.relationship('Subscript',backref='movie')


    def __repr__(self):
        return '<Movie %s>' %(self.name)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    logo=db.Column(db.String(200),unique=True)
    add_time = db.Column(db.DateTime, default=datetime.utcnow())



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.utcnow())
    password=db.Column(db.String(200))
    email=db.Column(db.String(50),unique=True)
    face=db.Column(db.String(200),unique=True)
    phone = db.Column(db.String(20))
    gender=db.Column(db.Boolean)
    info=db.Column(db.Text)

    comment=db.relationship('Comment',backref='user')
    subscript=db.relationship('Subscript',backref='user')
    userLog=db.relationship('UserLog',backref='user')



    def check(self,pwd):
        return check_password_hash(self.password,pwd)

    def __repr__(self):
        return '<User %s>' %(self.name)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text)
    add_time = db.Column(db.DateTime, default=datetime.utcnow())

    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    movie_id=db.Column(db.Integer,db.ForeignKey('movie.id'))

    def __repr__(self):
        return '<Comment %s>' %(self.content[:6])


class Subscript(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime, default=datetime.utcnow())
    movie_id=db.Column(db.Integer,db.ForeignKey('movie.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))


    def __repr__(self):
        return '<Subscript %s>' %(self.id)


class UserLog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime, default=datetime.utcnow())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    ip=db.Column(db.String(30))
    area=db.Column(db.String(50))

    def __repr__(self):
        return '<UserLog %s>' %(self.ip)


class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime, default=datetime.utcnow())
    name=db.Column(db.String(30),unique=True)
    url=db.Column(db.String(20),unique=True)

    role_id=db.Column(db.Integer,db.ForeignKey('role.id'))
    def __repr__(self):
        return '<Auth %s>' %(self.name)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime, default=datetime.utcnow())
    name = db.Column(db.String(30), unique=True)

    auth=db.relationship('Auth',backref='role')
    admin=db.relationship('Admin',backref='role')
    def __repr__(self):
        return '<Role %s>' %(self.name)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime, default=datetime.utcnow())
    name=db.Column(db.String(30), unique=True)
    password=db.Column(db.String(100))
    is_super=db.Column(db.Boolean,default=False)
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'))
    adminLog=db.relationship('AdminLog',backref='admin')
    adminOpLog=db.relationship('AdminOpLog',backref='admin')


    def check(self,pwd):
        return check_password_hash(self.password,pwd)


    def __repr__(self):
        return '<Admin %s>' %(self.name)

class AdminLog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime, default=datetime.utcnow())

    admin_id=db.Column(db.Integer,db.ForeignKey('admin.id'))
    ip=db.Column(db.String(30))
    area=db.Column(db.String(30))


    def __repr__(self):
        return '<AdminLog %s>' %(self.ip)


class AdminOpLog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    add_time = db.Column(db.DateTime, default=datetime.utcnow())
    reason=db.Column(db.String(100))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(30))
    area=db.Column(db.String(30))

    def __repr__(self):
        return "<AdminOpLog %s>" %(self.reason[:6])