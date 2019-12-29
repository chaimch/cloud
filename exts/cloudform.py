from wtforms import Form, fields

from const.enum import ResponseCodeEnum


class BaseForm(Form):
    resource = fields.FileField()

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
