class BpConfig:
    """蓝图配置"""
    from bp.mysql_bp import mysql_bp
    from bp.redis_bp import redis_bp

    BP_SUFFIX = 'BP'

    MYSQL_BP = mysql_bp
    REDIS_BP = redis_bp


class BaseConfig(BpConfig):
    DEBUG = False
    TESTING = False

    @property
    def DATABASE_URI(self):
        return 'sqlite:///:memory:'
