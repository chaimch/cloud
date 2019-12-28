"""请求序列化
    1. 兼容docker相关操作执行后返回结果为bytes情况
"""
from time import mktime


class CloudResponse:

    def __init__(self, response=None):
        self._response = self.__class__._serialize(response)

    @classmethod
    def _serialize(cls, response):
        """序列化"""
        if not isinstance(response, dict):
            return response

        # 如果是字节类型转为utf8
        if isinstance(response.get('data', ''), bytes):
            response['data'] = str(response['data'], encoding="utf-8")

        # 兼容json与usjon的, 结合flask_restful使用还需在loads回来, 有点多余, 待优化
        try:
            import ujson as json
            response = json.dumps(response)
        except:
            import json
            response = json.dumps(response, default=cls._json_default)
        finally:
            import json
            response = json.loads(response)

        return response

    @classmethod
    def _dt_to_ts(cls, dt):
        """datetime => 6位小数时间戳"""
        return mktime(dt.timetuple()) + dt.microsecond * 0.000001

    def _json_default(self, dt):
        """默认json序列化格式"""
        from datetime import datetime, date
        if isinstance(dt, (datetime, date)):
            return self._dt_to_ts(dt)
        raise TypeError('Type %s not serialzable' % type(dt))

    @property
    def response(self):
        return self._response
