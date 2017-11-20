#!encoding:utf-8
from flask import Flask, render_template
from app.config import config
from app.extensions import bootstrap, db, mail, moment, login_manage, photos
from .views import DEFAULT_BLUEPRINT
from flask_uploads import configure_uploads, patch_request_class


def create_app(config_name):
    # 创建应用实例
    app = Flask(__name__)
    # 初始化配置
    app.config.from_object(config[config_name])
    # 调用初始化函数
    config[config_name].init_app(app)
    # 配置相关扩展
    config_extensions(app)
    # 配置相关蓝本
    config_blueprint(app)
    # 配置错误显示
    config_errorhandler(app)
    # 返回应用实例
    return app


def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manage.init_app(app)
    login_manage.session_protection = 'strong'
    login_manage.login_view = 'user.login'
    login_manage.login_message = '请先登录'
    configure_uploads(app, photos)
    patch_request_class(app, size=None)


def config_blueprint(app):
    for blue_print, url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blue_print, url_prefix=url_prefix)


def config_errorhandler(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html')
