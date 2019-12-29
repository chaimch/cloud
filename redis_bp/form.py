from wtforms import fields
from wtforms import validators

from const.enum import ImageType, ContainerStatus
from exts.cloudform import BaseForm


class RedisInstanceForm(BaseForm):
    """redis instance的form校验类"""
    image_name = fields.StringField(validators=[validators.DataRequired(message='请填写镜像名称')])
    name = fields.StringField(validators=[validators.DataRequired(message='请填写容器名称')])
    ports = fields.FileField(validators=[validators.DataRequired(message='请填写端口配置')])
    mem_limit = fields.IntegerField(validators=[validators.DataRequired(message='请填写内存容量上限')])
    resource = fields.FileField(validators=[validators.DataRequired(message='请传入resource')])

    def validate_image_name(self, field):
        image_name = field.data
        if image_name != ImageType.redis.name:
            raise validators.ValidationError(f'{image_name}镜像不支持')

    def validate_name(self, field):
        name = field.data
        resource = self.resource.data

        container = resource.get_container(name=name)
        if container:
            raise validators.ValidationError(f'[{name}]容器已存在, 当前状态: {container.status}')


class RedisConfigForm(BaseForm):
    """redis config的form校验类"""
    name = fields.StringField(validators=[validators.DataRequired(message='请填写容器名称')])
