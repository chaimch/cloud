from config.devconfig import BaseDevConfig
from config.prodconfig import BaseProdConfig
from config.testconfig import BaseTestConfig


class DevConfig(BaseDevConfig):
    """开发配置"""
    pass


class TestConfig(BaseTestConfig):
    """测试环境配置"""
    pass


class ProdConfig(BaseProdConfig):
    """生产环境配置"""
    pass
