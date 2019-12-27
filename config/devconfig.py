from config.baseconfig import BaseConfig


class BaseDevConfig(BaseConfig):
    """开发配置基类"""
    DEBUG = True
    TESTING = True
