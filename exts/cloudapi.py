from functools import wraps

from flask import Blueprint
from flask_restful import Api
from werkzeug.wrappers import Response as ResponseBase

from const.enum import ResponseCodeEnum, ResponseMsgEnum


class CloudAPi(Api):
    def output(self, resource):
        """Wraps a resource (as a flask view function), for cases where the
        resource does not directly return a response object

        :param resource: The resource as a flask view function
        """

        @wraps(resource)
        def wrapper(*args, **kwargs):
            resp = resource(*args, **kwargs)

            if isinstance(resp, ResponseBase):
                return resp

            resp = self._cloud_extend_unpack(resp)
            data, code, headers = self._unpack(resp)

            data = self._serialize(data)

            return self.make_response(data, code, headers=headers)

        return wrapper

    @classmethod
    def _cloud_extend_unpack(cls, rv):
        """format response value"""
        code = None
        msg = None
        status = 200
        headers = {}

        # 如果返回值是元祖类型, 进行解包
        if isinstance(rv, tuple):
            len_rv = len(rv)

            if len_rv == 5:
                rv, code, msg, status, headers = rv
            elif len_rv == 4:
                rv, code, msg, status = rv
            elif len_rv == 3:
                rv, code, msg = rv
            elif len_rv == 2:
                rv, code = rv
            elif len_rv == 1:
                rv = list(rv)
            else:
                raise TypeError(
                    "The view function did not return a valid response tuple."
                    " The tuple must have the form (data, code, msg, status, headers),"
                    "or (data, code, msg, status), or (data, code, msg, status),"
                    "or (data, code, msg) or (data, code)"
                )
        elif rv is None:
            rv = rv

        if not isinstance(headers, dict):
            raise TypeError(
                "The view function did not return a valid response tuple."
                " The tuple must have the form (data, code, msg, status, headers),"
                "or (data, code, msg, status), or (data, code, msg, status),"
                "or (data, code, msg) or (data, code)"
            )

        resp = {
            'code': code or ResponseCodeEnum.ok,
            'data': rv,
            'msg': msg or ResponseMsgEnum.ok
        }
        flask_rv = (resp, status, headers)
        return flask_rv

    @classmethod
    def _unpack(cls, value):
        """Return a five tuple of data, code, msg, status, and headers"""
        if not isinstance(value, tuple):
            return value, 200, {}

        try:
            data, code, headers = value
            return data, code, headers
        except ValueError:
            pass

        try:
            data, code = value
            return data, code, {}
        except ValueError:
            pass

        return value, 200, {}

    def _serialize(self, resp):
        app = self.app
        if isinstance(app, Blueprint):
            from flask import current_app as _app
            app = _app
        serialize_cls = app.config.get('DEFAULT_SERIALIZE_CLS')
        if not serialize_cls:
            return
        return serialize_cls(resp).response
