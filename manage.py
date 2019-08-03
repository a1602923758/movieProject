
from app import manage, db
from app.models import *
from werkzeug.security import generate_password_hash
from flask_migrate import MigrateCommand
@manage.command
def initdb():
    """初始化数据库"""
    db.drop_all()
    db.create_all()
    u=User(name='westos',password=generate_password_hash('westos123'),email='westos@qq.com')
    db.session.add(u)
    db.session.commit()
    print('初始化数据库成功')

@manage.command
def createAdmin():
    """创建管理员"""
    name=input('输入管理员帐号')
    password=input('输入管理员密码')
    admin=Admin(name=name,password=generate_password_hash(password),is_super=True)
    db.session.add(admin)
    db.session.commit()
    print('创建管理员成功')




manage.add_command('db',MigrateCommand)
if __name__ == '__main__':
    manage.run()
