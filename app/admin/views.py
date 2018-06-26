import uuid

from flask import Blueprint, render_template, redirect, url_for, flash, session, request, app
from app.admin.forms import LoginFrom, TagForm, MovieForm
from app.exit import db, init_up_config
from app.home.models import Admin, Tag, Movie
from functools import wraps
# 通过工具引入
from werkzeug.utils import secure_filename
import os
import datetime

admin = Blueprint('admin', __name__)


@admin.route('/')
def index():
    return render_template('admin/index.html')


# 定义登陆的装饰器, 不登陆就不能查看
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for('admin.index', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 定义一个方法修改文件名称
def change_filename(filename):
    # 分割文件后缀名
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename

@admin.route('/login/', methods=['GET', 'POST'])
def login():
    # 实例化登陆表单
    form = LoginFrom()
    # 提交的的时候获取验正
    if form.validate_on_submit():
        # 获取表单的数据
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        # 密码错误时，check_pwd返回false,则此时not check_pwd(data["pwd"])为真。
        if not admin.check_pwd(data['pwd']):
            # 消息闪现
            flash('密码错误')
            return redirect(url_for('admin.login'))
        # 如果是正确的，就要定义session的会话进行保存。
        session['admin'] = data['account']
        # return redirect(request.args.get('next')) or url_for('admin.index')
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html', form=form)


@admin.route('/logout/')
@admin_login_req
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


@admin.route('/pwd/')
@admin_login_req
def pwd():
    return render_template('admin/pwd.html')


# 添加标签
@admin.route('/tag/add/', methods=['GET', 'POST'])
# @admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data['name']).count
        if tag == 1:
            flash('名称已经存在', 'err')
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            name=data['name']
        )
        db.session.add(tag)
        db.session.commit()
        flash('添加标签成功', 'ok')
        redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html', form=form)


# 标签列表
@admin.route('/tag/list/<int:page>/', methods=['GET', 'POST'])
# @admin_login_req
def tag_list(page=None):
    # 查询和分页的显示
    if page is None:
        page = 1
    page_data = Tag.query.order_by(Tag.addtime.desc()).paginate(page=page, per_page=10)
    return render_template('admin/tag_list.html', page_data=page_data)


# 标签的删除
@admin.route('/tag/del/<int:id>/', methods=['GET', 'POST'])
# @admin_login_req
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除标签成功', 'ok')
    return redirect(url_for('admin.tag_list', page=1))


# 编辑标签
@admin.route('/tag/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
def tag_edit(id):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count
        if tag.name != data['name'] and tag_count == 1:
            flash('标签已经存在', 'err')
            return redirect(url_for('admin.tag_edit'))
        tag = Tag(
            name=data['name']
        )
        db.session.add(tag)
        db.session.commit()
        flash('修改白标签成功', 'ok')
        redirect(url_for('admin.tag_edit', id=id))
    return render_template('admin/tag_add.html', form=form, tag=tag)


@admin.route('/movie/add/', methods=['GET', 'POST'])
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        # 获取上传文件的url
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(init_up_config(app)):
            os.makedirs(init_up_config(app))
            #     授权 可读,可写
            os.chmod(init_up_config(app), 777)
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(init_up_config(app) + url)
        form.url.data.save(init_up_config(app) + logo)
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data["star"]),
            playnum=0,
            commentnum=0,
            tag_id=int(data["tag_id"]),
            area=data["area"],
            release_time=data["release_time"],
            length=data["length"]
        )
        db.session.add(movie)
        db.session.commit()
        flash("添加电影成功！", "ok")
        return redirect(url_for('admin.movie_add'))
    return render_template("admin/movie_add.html", form=form)


@admin.route('/movie/list/')
@admin_login_req
def movie_list():
    return render_template('admin/movie_list.html')


@admin.route('/preview/add/')
@admin_login_req
def preview_add():
    return render_template('admin/preview_add.html')


@admin.route('/preview/list/')
@admin_login_req
def preview_list():
    return render_template('admin/preview_list.html')


@admin.route('/user/list/')
@admin_login_req
def user_list():
    return render_template('admin/user_list.html')


@admin.route('/user/view/')
@admin_login_req
def user_view():
    return render_template('admin/user_view.html')


@admin.route('/comment/list/')
@admin_login_req
def comment_list():
    return render_template('admin/comment_list.html')


@admin.route('/moviecol/list/')
@admin_login_req
def moviecol_list():
    return render_template('admin/moviecol_list.html')


@admin.route('/oplog/list/')
@admin_login_req
def oplog_list():
    return render_template('admin/oplog_list.html')


@admin.route('/adminloginlog/list/')
@admin_login_req
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')


@admin.route('/userloginlog/list/')
@admin_login_req
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')


@admin.route('/role/add/')
@admin_login_req
def role_add():
    return render_template('admin/role_add.html')


@admin.route('/role/list/')
@admin_login_req
def role_list():
    return render_template('admin/role_list.html')


@admin.route('/auth/add/')
@admin_login_req
def auth_add():
    return render_template('admin/auth_add.html')


@admin.route('/auth/list/')
@admin_login_req
def auth_list():
    return render_template('admin/auth_list.html')


@admin.route('/admin/add/')
@admin_login_req
def admin_add():
    return render_template('admin/admin_add.html')


@admin.route('/admin/list/')
@admin_login_req
def admin_list():
    return render_template('admin/admin_list.html')
