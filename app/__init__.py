from flask import Flask, render_template

from app.admin.views import admin
from app.exit import init_ext
from app.home.views import home

app = Flask(__name__)
app.debug = True


def create_app():
    init_ext(app=app)
    register_blue()
    return app


def register_blue():
    app.register_blueprint(home, url_prefix='/home')
    app.register_blueprint(admin, url_prefix='/admin')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404
