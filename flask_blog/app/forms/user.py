from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, EqualTo, Email, Length
from app import photos
from app.models import User
from flask_login import current_user
from werkzeug.security import check_password_hash


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(6, 18, message='用户名长度必须在6~18个字符之间')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 18, message='密码长度必须在6~18个字符之间')])
    confirm = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message='两次输入的密码不一致')])
    email = StringField('邮箱', validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('立即注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    password = PasswordField('密码', validators=[DataRequired('请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

    # def validate_username(self, field):
    #     if User.query.filter_by(username=field.username.data):
    #         return True
    #     raise ValidationError('用户名错误')
    #
    # def validate_password(self, field):
    #     pass


class ChangPwdForm(FlaskForm):
    oldpsw = PasswordField('原密码')
    psw = PasswordField('新密码', validators=[DataRequired(message='请输入密码'), Length(6, 18, message='密码长度必须在6~18个字符之间')])
    confirm_psw = PasswordField('确认密码', validators=[EqualTo('psw',message='两次输入的密码不同')])
    submit = SubmitField('提交')

    def validate_oldpsw(self, field):
        if check_password_hash(current_user.password_hash, field.data):
            pass
        else:
            raise ValidationError('原密码错误')


class ChangEmailForm(FlaskForm):
    oldemail = StringField('原邮箱')
    email = StringField('新邮箱', validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('提交')

    def validate_oldemail(self, field):
        if current_user.email != field.data:
            raise ValidationError('原邮箱错误')


class IconForm(FlaskForm):
    icon = FileField('头像', validators=[FileRequired(message='请选择文件'), FileAllowed(photos, message='文件格式不支持')])
    submit = SubmitField('提交')
