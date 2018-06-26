from flask import Blueprint, redirect, url_for

from app.exit import db
from app.home.models import Role, Admin
# 导入加密工具
from werkzeug.security import generate_password_hash
from flask import render_template

home = Blueprint('home', __name__)


# 测试加入数据
@home.route('/add/')
def add():
    # role = Role(name='超级管理员', auths="")
    # admin = Admin(name='like', pwd=generate_password_hash('123456'), is_super=0, role_id=1)
    admin = Admin(name='123', pwd=generate_password_hash('123456'), is_super=0, role_id=1)
    # db.session.add(role)
    db.session.add(admin)
    db.session.commit()
    return 'success'


# @home.route('/')
# def index():
#     return render_template('home/index.html')


@home.route('/login/')
def login():
    return render_template('home/login.html')


@home.route('/logout/')
def logout():
    return redirect(url_for('home.login'))


@home.route('/register/')
def register():
    return render_template('home/register.html')


@home.route('/user/')
def user():
    return render_template('home/user.html')\

@home.route('/pwd/')
def pwd():
    return render_template('home/pwd.html')
@home.route('/comments/')
def comments():
    return render_template('home/comments.html')

@home.route('/')
def index():
    return render_template('home/index.html')


@home.route('/animation/')
def animation():
    return render_template('home/animation.html')


@home.route('/loginlog/')
def loginlog():
    return render_template('home/loginlog.html')


@home.route('/moviecol/')
def moviecol():
    return render_template('home/moviecol.html')

@home.route('/search/')
def search():
    return render_template('home/search.html')

@home.route('/play/')
def play():
    return render_template('home/play.html')
