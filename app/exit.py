import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def init_ext(app: Flask):
    # 初始化数据库相关的配置
    init_config(app)
    # 配置文件上传
    init_up_config(app)


def init_config(app):
    app.config['SECRET_KEY'] = 'aefe8fded8724467b3741af506434ccd'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/movie?charset=utf8'
    db.init_app(app)
    migrate.init_app(app, db)


def init_up_config(app):
    # app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/upload')
    app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
