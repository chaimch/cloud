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

    def validate_image_name(self, field):
        image_name = field.data
        if image_name != ImageType.redis.name:
            raise validators.ValidationError(f'{image_name}镜像不支持')

    def validate_name(self, field):
        name = field.data
        resource = self.resource.data

        container = resource.get_container(name=name)
        if container and container.status == ContainerStatus.running.name:
            raise validators.ValidationError(f'[{name}]容器已存在, 当前状态: {container.status}')

    def validate_ports(self, field):
        """校验端口是否被占用"""
        ports = field.data
        resource = self.resource.data
        for source_port_and_protocol, target_port in ports.items():
            source_port, _ = source_port_and_protocol.split('/')
            try:
                source_port = int(source_port)
            except Exception as e:
                raise validators.ValidationError(f'invalid  ports, {ports}')

            free_port = resource.get_free_port(source_port)
            if not free_port:
                raise validators.ValidationError('无可用端口, 请稍后再试')

            if free_port != source_port:
                raise validators.ValidationError(f'{source_port} 端口已被占用, 推荐使用{free_port}端口')


class RedisConfigForm(BaseForm):
    """redis config的form校验类"""
    name = fields.StringField(validators=[validators.DataRequired(message='请填写容器名称')])

    def validate_name(self, field):
        name = field.data
        resource = self.resource.data

        if not resource.get_container(name=name):
            raise validators.ValidationError(f'[{name}]容器不存在')
