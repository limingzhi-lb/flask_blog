import os

base_dir = os.path.abspath(os.path.dirname(__file__))
# 通用配置
class Config:
    # 秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you guess you can guess it but you never guess it'
    # 数据库操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '17865923550@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'zhi8023ming'
    # bootstrap使用本地库中的依赖包
    BOOTSTRAP_SERVE_LOCAL = True
    # 文件上传
    MAX_CONTENT_LENGTH = 12 * 1024 * 1024
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload')
    # 初始化方法
    @staticmethod
    def init_app(app):
        pass


# 开发环境配置
class DevelopmentConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:lmz1995@localhost/flask'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog.sqlite')


# 测试环境配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:lmz1995@localhost/flask'


# 生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:lmz1995@localhost/flask'


# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    # 默认配置
    'default': DevelopmentConfig
}