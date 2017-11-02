import os
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from app.forms import RegisterForm, LoginForm, UploadPhoto
from app.models import User
from app.extensions import db, photo
from app.email import send_mail
from flask_login import login_user,logout_user, login_required, current_user
from PIL import Image

user = Blueprint('user', __name__)

# 注册
@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, password=form.password.data,
                 email=form.email.data)
        db.session.add(u)
        db.session.commit()
        token = u.generate_activate_token()
        send_mail(form.email.data, '账户激活', 'email/account_activate',
                  token=token, username=form.username.data)
        flash('激活邮件已发送，请点击链接完成用户激活')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)

@user.route('/activate/<token>/')
def activate(token):
    if User.check_activate_token(token):
        flash('账户激活成功')
        return redirect(url_for('user.login'))
    else:
        flash('账户激活失败')
        return redirect(url_for('main.index'))


# 登录
@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is None:
            flash('此用户不存在~~~')
        elif u.verify_password(form.password.data):
            # 验证通过，用户登录，顺便可以完成记住的功能
            login_user(u, remember=form.remember_me.data)
            # 如果有下一跳转地址就跳转到指定地址，没有跳转到首页
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('密码不对哦~~')
    return render_template('user/login.html', form=form)

# 退出账号
@user.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录~~~')
    return redirect(url_for('main.index'))

# 生成随机的字符串
def rand_str(length=32):
    import random
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(random.choice(base_str) for i in range(length))
@user.route('/upload_photo/', methods=['GET','POST'])
@login_required
def upload_photo():
    form = UploadPhoto()
    if form.validate_on_submit():
        # 获得上传图片的后缀
        suffix = os.path.splitext(form.photo.data.filename)[1]
        name = rand_str() + suffix
        # 保存上传图片
        photo.save(form.photo.data, name=name)
        # 获得图片保存的路径位置
        photoname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], name)
        # 对该图片进行缩略
        img = Image.open(photoname)
        img.thumbnail((128, 128))
        img.save(photoname)
        # 将上一次的头像删除
        if current_user.photo_url != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.photo_url))
        # 保存图片的名字到user表中
        current_user.photo_url = name
        db.session.add(current_user)
        flash('你的头像已更换~~~')
    return render_template('user/upload_photo.html', form=form)

# 个人信息展示
@user.route('/profile/')
@login_required
def profile():
    return render_template('user/profile.html')


