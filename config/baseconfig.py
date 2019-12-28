class BpConfig:
    """蓝图配置"""
    BP_SUFFIX = 'BP'

    from mysql_bp import urls as mysql_server_urls
    MYSQL_URLS = mysql_server_urls

    from mysql_bp.server import mysql_bp
    MYSQL_BP = mysql_bp

    from redis_bp import urls as redis_server_urls
    REDIS_URLS = redis_server_urls

    from redis_bp.server import redis_bp
    REDIS_BP = redis_bp


class SerializeConfig:
    """序列化配置"""
    from exts.serialize import CloudResponse
    DEFAULT_SERIALIZE_CLS = CloudResponse


class BaseConfig(BpConfig, SerializeConfig):
    DEBUG = False
    TESTING = False

    @property
    def DATABASE_URI(self):
        return 'sqlite:///:memory:'
