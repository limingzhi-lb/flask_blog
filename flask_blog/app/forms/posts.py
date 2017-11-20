from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostsForm(FlaskForm):
    content = TextAreaField('', render_kw={'placeholder': '这一刻的想法...'}, validators=[DataRequired(message='请输入内容'), Length(1, 128, message='过长')])
    submit = SubmitField('发表')


class CommentForm(FlaskForm):
    content = TextAreaField('', render_kw={'placeholder': '说点什么吧'}, validators=[DataRequired(message='请输入内容'), Length(1, 128, message='过长')])
    submit = SubmitField('评论')


class ResponseForm(FlaskForm):
    content = TextAreaField('', render_kw={'placeholder': '回复该用户'}, validators=[DataRequired(message='请输入内容'), Length(1, 128, message='过长')])
    submit = SubmitField('回复')
