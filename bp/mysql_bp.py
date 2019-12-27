from flask import Blueprint

mysql_bp = Blueprint('mysql_bp', __name__, url_prefix='/api/mysql')


@mysql_bp.route("/create_instance", methods=["POST"])
def mysql_instance_create():
    return "Mysql instance has been created"


@mysql_bp.route("/get_config")
def mysql_config_get():
    return "Mysql config"
