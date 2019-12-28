from flask import Blueprint

from exts.cloudapi import CloudAPi
from mysql_bp.server import MysqlConfigServer
from mysql_bp.server import MysqlInstanceServer

mysql_bp = Blueprint('mysql_bp', __name__, url_prefix='/api/mysql')
mysql_server_api = CloudAPi(mysql_bp)

mysql_server_api.add_resource(MysqlInstanceServer, '/create_instance')
mysql_server_api.add_resource(MysqlConfigServer, '/get_config')
