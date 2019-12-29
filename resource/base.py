import logging
import string
from random import choice

from flask import request
from flask_restful import Resource

from const.enum import ResponseCodeEnum, ResponseMsgEnum


class BaseResource(Resource):

    def __init_hook__(self):
        self.hook_before_request_func_list = []
        self.hook_after_request_func_list = []

        self.params = {}
        self.before_request_register(self.check_params)

    def before_request_register(self, func):
        self.hook_before_request_func_list.append(func)

    def parse_params(self):
        self.params.update(request.args.to_dict() or {})
        self.params.update(request.get_json() or {})

    def check_params(self, *args, **kwargs):
        """子类自行实现"""

    def before_request(self, *args, **kwargs):
        """请求前钩子"""
        self.parse_params()
        resp = None
        for func in self.hook_before_request_func_list:
            resp = resp or func(*args, **kwargs)
        return resp

    def dispatch_request(self, *args, **kwargs):
        """请求分发处理"""
        self.__init_hook__()
        resp = self.before_request(*args, **kwargs)
        if not resp:
            try:
                resp = super().dispatch_request(*args, **kwargs)
            except Exception as e:
                logging.exception(e)
                resp = str(e), ResponseCodeEnum.inner_error, ResponseMsgEnum.inner_error
            self.after_request(resp, *args, **kwargs)
        return resp

    def after_request(self, resp, *args, **kwargs):
        """请求后钩子"""
        for func in self.hook_after_request_func_list:
            func(resp, *args, **kwargs)

    @classmethod
    def generate_password(cls, length=16, chars=string.ascii_letters + string.digits):
        """指定位数, 随机密码生成"""
        return ''.join([choice(chars) for i in range(length)])
