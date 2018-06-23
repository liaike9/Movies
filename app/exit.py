from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def init_ext(app:Flask):
    # 初始化数据库相关的配置
    init_config(app)



def init_config(app):
    app.config['SECRET_KEY']='1213'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/movie?charset=utf8'
    db.init_app(app)
    migrate.init_app(app, db)
