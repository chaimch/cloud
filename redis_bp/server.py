from flask import Blueprint
from flask_restful import Resource

redis_bp = Blueprint('redis_bp', __name__, url_prefix='/api/redis')


class RedisInstanceServer(Resource):
    def post(self):
        """创建redis实例"""
        return "Redis instance has been created"


class RedisConfigServer(Resource):
    def get(self):
        """获取redis配置"""
        return "redis config"
