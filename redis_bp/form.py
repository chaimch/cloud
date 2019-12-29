from wtforms import fields, validators

from const.enum import ImageType
from resource.base import BaseForm


class RedisInstanceForm(BaseForm):
    """redis instance的form校验类"""
    image_name = fields.StringField(validators=[validators.DataRequired(message='请填写镜像名称')])
    name = fields.StringField(validators=[validators.DataRequired(message='请填写容器名称')])
    ports = fields.FileField(validators=[validators.DataRequired(message='请填写端口配置')])
    mem_limit = fields.IntegerField(validators=[validators.DataRequired(message='请填写内存容量上限')])

    def validate_image_name(self, field):
        image_name = field.data
        if image_name != ImageType.redis.name:
            raise validators.ValidationError(f'{image_name}镜像不支持')


class RedisConfigForm(BaseForm):
    """redis config的form校验类"""
    name = fields.StringField(validators=[validators.DataRequired(message='请填写容器名称')])
