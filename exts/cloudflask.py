import os

from flask import Flask


class CloudFlask(Flask):
    @classmethod
    def create_app(cls, config_dot_path=None, import_name=None):
        """创建app"""
        self = cls(import_name or __name__)

        self._parse_config(config_dot_path)

        self.dynamic_register()

        return self

    def _parse_config(self, config_dot_path=None):
        """解析配置"""
        config_dot_path = config_dot_path or os.getenv('FLASK_CONFIG', 'config.DevConfig')
        self.config.from_object(config_dot_path)

    def dynamic_register(self):
        """动态代理注册"""
        for may_bp in self.config:
            if not self._is_blueprint_cfg(may_bp):
                continue
            self.register_blueprint(self.config[may_bp])

    def _is_blueprint_cfg(self, may_bp_cfg):
        """是否是bp的配置"""
        bp_suffix = self.config['BP_SUFFIX']
        return isinstance(may_bp_cfg, str) and may_bp_cfg.split('_')[-1] == bp_suffix