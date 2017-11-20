from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_required
from app.forms import PostsForm, CommentForm, ResponseForm
from app.models import Posts, User
from app.extensions import db
from datetime import datetime


main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
def index():
    form = PostsForm()
    u = current_user._get_current_object()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            p = Posts(content=form.content.data, timestamp=datetime.now(), user=u)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('请先登录')
            return redirect(url_for('user.login'))
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(rid=0, rrid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=3, error_out=True)
    posts = pagination.items
    return render_template('main/index.html', form=form, posts=posts, pagination=pagination)


@main.route('/post_list/')
@login_required
def post_list():
    name = request.args.get('name')
    if name:
        session['name'] = name
    else:
        name = session['name']
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(rid=0, rrid=0, uid=User.query.filter_by(username=name).first().id).order_by(Posts.timestamp.desc()).paginate(page, per_page=3, error_out=True)
    post_list = pagination.items
    return render_template('main/post_list.html', post_list=post_list, pagination=pagination, name=name)


@main.route('/comment/', methods=['POST', 'GET'])
@login_required
def comment():
    response = request.args.get('response')
    if response:
        form = ResponseForm()
    else:
        response = 0
        form = CommentForm()
    if form.validate_on_submit():
        comment = Posts(content=form.content.data, uid=current_user.id, rid=session['post_id'], rrid=response)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.comment'))
    post_id = request.args.get('post_id')
    if post_id:
        session['post_id'] = post_id
    else:
        post_id = session['post_id']
    post = Posts.query.get(post_id)
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(rid=post_id, rrid=0).order_by(Posts.timestamp.desc()).paginate(page, per_page=3, error_out=True)
    comment_list = pagination.items
    response_dict = {}
    for comment in comment_list:
        resp = Posts.query.filter_by(rrid=comment.id).order_by(Posts.timestamp.desc())
        response_dict[comment.id] = resp
    return render_template('main/post_comment.html', comment_list=comment_list, pagination=pagination, post=post, form=form, response_dict=response_dict)


@main.route('/response/', methods=['POST','GET'])
def response():
    form = ResponseForm()
