from flask import Blueprint

redis_bp = Blueprint('redis_bp', __name__, url_prefix='/api/redis')


@redis_bp.route("/create_instance", methods=["POST"])
def redis_instance_create():
    return "Redis instance has been created"


@redis_bp.route("/get_config")
def redis_config_get():
    return "Redis config"
