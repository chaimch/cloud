from flask import Flask


class CloudFlask(Flask):

    @classmethod
    def create_app(cls, import_name=None):
        flask_app = cls(import_name or __name__)

        flask_app.dynamic_register()

        return flask_app

    def dynamic_register(self):
        """动态代理注册
            1. TODO: 待通过动态导入bp包下内容来实现动态注册
        """
        from bp.mysql_bp import mysql_bp
        from bp.redis_bp import redis_bp

        self.register_blueprint(mysql_bp)
        self.register_blueprint(redis_bp)


app = CloudFlask.create_app()
