from flask import Blueprint

from resource.docker import DockerResource

mysql_bp = Blueprint('mysql_bp', __name__, url_prefix='/api/mysql')


class MysqlInstanceServer(DockerResource):
    def post(self):
        """创建mysql实例"""
        res = self.docker_client.containers.run("ubuntu", "echo hello world")
        return res, 0, 'ok'


class MysqlConfigServer(DockerResource):
    def get(self):
        """获取mysql配置"""
        return "Mysql config"
