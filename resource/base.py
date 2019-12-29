from flask import request
from flask_restful import Resource
from wtforms import Form

from const.enum import ResponseCodeEnum


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
            resp = super().dispatch_request(*args, **kwargs)
            self.after_request(resp, *args, **kwargs)
        return resp

    def after_request(self, resp, *args, **kwargs):
        """请求后钩子"""
        for func in self.hook_after_request_func_list:
            func(resp, *args, **kwargs)


class BaseForm(Form):

    def check(self):
        """检验form"""

        is_ok, error_msg = self.validate(), ""
        if not is_ok:
            error_msg = self._get_error_msg()

        return is_ok, error_msg

    def _get_error_msg(self):
        """获取错误信息"""
        error_msg = '内部错误'

        error_keys = list(self.errors.keys())
        if not error_keys:
            return error_msg

        first_error_key = error_keys[0]
        if not first_error_key:
            return error_msg

        error_msg = self.errors[first_error_key][-1]
        return error_msg

    def check_for_return(self):
        is_ok, error_msg = self.check()

        # 检验通过, 直接返回
        if is_ok:
            return

        # 校验未通过, 组装返回格式
        return {}, ResponseCodeEnum.wrong_args, error_msg
