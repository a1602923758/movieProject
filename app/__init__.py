from flask import Flask

from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
import pymysql
# 当调用这个连接数据库的函数时，任何应用导入Mysqldb连接数据库，
# 实际上是使用的是pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)

app.config.from_pyfile('../config.py')

db=SQLAlchemy(app)
manage=Manager(app)
bt=Bootstrap(app)
moment=Moment(app)
migrate=Migrate(app,db)
from app.admin import admin as admin_bp
from app.home import home as home_bp
app.register_blueprint(admin_bp,url_prefix='/admin')
app.register_blueprint(home_bp)






