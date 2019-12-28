from flask_restful import Api

from bp.mysql_bp import MysqlConfigServer
from bp.mysql_bp import MysqlInstanceServer
from bp.mysql_bp import mysql_bp
from bp.redis_bp import RedisConfigServer
from bp.redis_bp import RedisInstanceServer
from bp.redis_bp import redis_bp

mysql_server_api = Api(mysql_bp)
redis_server_api = Api(redis_bp)

mysql_server_api.add_resource(MysqlInstanceServer, '/create_instance')
mysql_server_api.add_resource(MysqlConfigServer, '/get_config')

redis_server_api.add_resource(RedisInstanceServer, '/create_instance')
redis_server_api.add_resource(RedisConfigServer, '/get_config')
