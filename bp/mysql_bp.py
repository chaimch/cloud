from flask import Blueprint
from flask_restful import Resource

mysql_bp = Blueprint('mysql_bp', __name__, url_prefix='/api/mysql')


class MysqlInstanceServer(Resource):
    def post(self):
        """创建mysql实例"""
        return "Mysql instance has been created"


class MysqlConfigServer(Resource):
    def get(self):
        """获取mysql配置"""
        return "Mysql config"
