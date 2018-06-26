# 登陆表单验证
from flask_wtf import FlaskForm
# 导入相应的字段
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, TextAreaField
# 导入验证器
from wtforms.validators import DataRequired, ValidationError

from app.home.models import Admin, Tag, Movie


class LoginFrom(FlaskForm):
    """
    管来员登陆表单
    validators" 验证器
    render_kw 附加选项
    """
    account = StringField(
        label='账号',
        validators=[DataRequired('请输入账号')],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            # "required": "required",
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[DataRequired('请输入密码')],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            # "required": "required",
        }
    )
    submit = SubmitField(
        "登陆",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    # 验证账号
    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError('账号不存在')


class TagForm(FlaskForm):
    name = StringField(
        label='名称',
        validators=[DataRequired('请输入标签')],
        description='标签',
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标签名称！",
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary",
        }
    )


#电影表单



class MovieForm(FlaskForm):
    title = StringField(
        label="片名",
        validators=[
            DataRequired("片名不能为空！")
        ],
        description="片名",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "请输入片名！"
        }
    )
    url = FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件！")
        ],
        description="文件",
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("简介不能为空！")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 10
        }
    )
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="封面",
    )
    star = SelectField(
        label="星级",
        validators=[
            DataRequired("请选择星级！")
        ],
        # star的数据类型
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description="星级",
        render_kw={
            "class": "form-control",
        }
    )
    # 标签要在数据库中查询已存在的标签
    # tag_id = SelectField(
    #     label="标签",
    #     validators=[
    #         DataRequired("请选择标签！")
    #     ],
    #     coerce=int,
    #     # 通过列表生成器生成列表
    #     # choices=[(v.id, v.name) for v in Tag.query.all()],
    #
    #     description="标签",
    #     render_kw={
    #         "class": "form-control",
    #     }
    # )
    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区！")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区！"
        }
    )
    length = StringField(
        label="片长",
        validators=[
            DataRequired("片长不能为空！")
        ],
        description="片长",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片长！"
        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("上映时间不能为空！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请选择上映时间！",
            "id": "input_release_time"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )

