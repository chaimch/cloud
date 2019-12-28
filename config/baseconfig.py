class BpConfig:
    """蓝图配置"""
    from bp import urls
    URLS = urls

    BP_SUFFIX = 'BP'

    from bp.mysql_bp import mysql_bp
    MYSQL_BP = mysql_bp

    from bp.redis_bp import redis_bp
    REDIS_BP = redis_bp


class BaseConfig(BpConfig):
    DEBUG = False
    TESTING = False

    @property
    def DATABASE_URI(self):
        return 'sqlite:///:memory:'
