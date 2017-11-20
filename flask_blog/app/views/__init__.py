#!encoding:utf-8
from .main import main
from .user import user


DEFAULT_BLUEPRINT = (
    # 蓝本  前缀
    (main, ''),
    (user, '/user')
)
