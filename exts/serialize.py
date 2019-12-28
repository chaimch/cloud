"""请求序列化
    1. 兼容docker相关操作执行后返回结果为bytes情况
"""
import json
from datetime import datetime, date
from time import mktime


class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

    @classmethod
    def _dt_to_ts(cls, dt):
        """datetime => 6位小数时间戳"""
        return mktime(dt.timetuple()) + dt.microsecond * 0.000001


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

        # 兼容json与usjon的, 结合flask_restful使用还需再loads回来, 有点多余, 待优化
        try:
            import ujson as json
            response = json.dumps(response)
        except Exception as e:
            import json
            response = json.dumps(response, cls=CJsonEncoder, skipkeys=True)
        finally:
            if isinstance(response, str):
                import json
                response = json.loads(response)

        return response

    @property
    def response(self):
        return self._response
