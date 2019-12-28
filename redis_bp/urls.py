from exts.cloudapi import CloudAPi
from redis_bp.server import RedisConfigServer
from redis_bp.server import RedisInstanceServer
from redis_bp.server import redis_bp

redis_server_api = CloudAPi(redis_bp)

redis_server_api.add_resource(RedisInstanceServer, '/create_instance')
redis_server_api.add_resource(RedisConfigServer, '/get_config')
