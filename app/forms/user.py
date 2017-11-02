# 导入表单基类
from flask_wtf import FlaskForm
# 导入相关字段
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
# 导入验证器类
from wtforms.validators import DataRequired, EqualTo, Email, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User
from app.extensions import photo

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(),
                                              Length(6, 18, message='用户名必须在6~18个字符之间')])
    password = PasswordField('密码', validators=[DataRequired(),
                                               Length(6, 18, message='密码必须在6~18个字符之间')])
    confirm = PasswordField('确认密码', validators=[DataRequired(),
                                                Length(6, 18, message='密码必须在6~18个字符之间'),
                                                EqualTo('password', message='两次密码不一致')])
    email = StringField('邮箱', validators=[Email(message='邮箱格式不对')])
    submit = SubmitField('立即注册')

    # 自定义验证器，验证用户名
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已存在')

    # 自定义验证器，验证邮箱
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已使用，请选用其他邮箱~~~')

# 用户登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

# 上传头像表单
class UploadPhoto(FlaskForm):
    photo = FileField('',validators=[FileAllowed(photo, message='只允许图片格式'),
                                  FileRequired('请上传头像~~~')])
    submit = SubmitField('上传头像')