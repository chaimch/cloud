import logging
import socket

from resource.base import BaseResource


class OSResource(BaseResource):
    def __init__(self):
        self.logger = self._get_default_logger()

    @classmethod
    def _get_default_logger(cls):
        """获取默认的logger"""
        logging.basicConfig(format='%(asctime)s.%(msecs)d  %(module)s:%(process)s  %(levelname)s  %(message)s',
                            level=logging.INFO)
        logger = logging.getLogger('OSResource')
        return logger

    @classmethod
    def check_port(cls, port, ip='0.0.0.0'):
        """端口占用校验"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, int(port)))
        return not result

    def get_free_port(self, port, ip='0.0.0.0', retry_times=16):
        """获取可用端口"""
        for i in range(retry_times):
            if not self.check_port(port, ip=ip):
                return port
            port += 2 ** i
            if port > 65536:
                break
        return 0
