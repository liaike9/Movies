from flask import Flask
from flask_migrate import MigrateCommand
from flask_script import Manager, Server

from app import create_app
from app.home.models import  *
app = create_app()
manager = Manager(app)
manager.add_command('start', Server(host='127.0.0.1', port=7000))
# 添加迁移脚本
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()
