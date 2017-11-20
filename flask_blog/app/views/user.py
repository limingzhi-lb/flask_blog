from flask import Blueprint, render_template, flash, url_for, redirect, current_app, request
from app.forms import RegisterForm, LoginForm, IconForm, ChangPwdForm, ChangEmailForm
from app.email import send_mail
from app.extensions import db, photos
import os
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.models import User
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from PIL import Image


user = Blueprint('user', __name__)


@user.route('/login/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('登录成功')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('登录失败')
    return render_template('user/login.html', form=form)


@user.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        token = s.dumps({'username': form.username.data})
        send_mail(form.email.data, '账户激活', 'email/account_activate', token=token, username=form.username.data)
        flash('用户注册完成，激活邮件以发送，请点击链接完成激活')
        user = User(username=form.username.data, password_hash=generate_password_hash(form.password.data), email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@user.route('/activate/<token>')
def activate(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return 'token有误'
    user = User.query.filter_by(username=data.get('username')).first()
    print(user.username)
    user.confirmed = True
    db.session.add(user)
    # db.session.commot()
    return '%s账户已经激活' % data.get('username')


@user.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@user.route('/profile/')
@login_required
def profile():
    print(current_user)
    return render_template('user/profile.html')


@user.route('/change_password/', methods=['POST', 'GET'])
@login_required
def change_password():
    form = ChangPwdForm()
    if form.validate_on_submit():
        print(current_user.username)
        user = User.query.filter_by(username=current_user.username).first()
        user.password_hash = generate_password_hash(form.psw.data)
        db.session.add(user)
        flash('修改成功，请重新登录')
        logout_user()
        return redirect(url_for('user.login'))

    return render_template('user/change_psw.html', form=form)


@user.route('/change_email/', methods=['POST', 'GET'])
@login_required
def change_email():
    form = ChangEmailForm()
    if form.validate_on_submit():
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        token = s.dumps({'username': current_user.username, 'email': form.email.data})
        send_mail(form.email.data, '邮箱修改', 'email/email_activate', token=token, username=current_user.username)
        flash('验证链接已发至新邮箱，请前往修改')
        return redirect(url_for('main.index'))
    return render_template('user/change_email.html', form=form)


@user.route('/email_activate/<token>')
def email_activate(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return '修改失败'
    user = User.query.filter_by(username=data.get('username')).first()
    user.email = data.get('email')
    db.session.add(user)
    flash('邮箱修改成功')
    logout_user()
    return render_template('main/index.html')


@user.route('/change_icon/', methods=['POST', 'GET'])
@login_required
def change_icon():
    form = IconForm()
    if form.validate_on_submit():
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))
        suffix = os.path.splitext(form.icon.data.filename)[-1]
        imgname = current_user.username+suffix
        photos.save(form.icon.data, name=imgname)
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], imgname)
        img = Image.open(pathname)
        img.thumbnail((64, 64))
        img.save(pathname)
        current_user.icon = imgname
        db.session.add(current_user)
        flash('头像已更换')
    return render_template('user/change_psw.html', form=form)