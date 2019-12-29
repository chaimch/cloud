from wtforms import fields
from wtforms import validators

from const.enum import ImageTypeEnum, ContainerStatusEnum, CharsetEnum
from exts.cloudform import BaseForm


class MysqlInstanceForm(BaseForm):
    """Mysql instance的form校验类"""
    image_name = fields.StringField(validators=[validators.DataRequired(message='请填写镜像名称')])
    name = fields.StringField(validators=[validators.DataRequired(message='请填写容器名称')])
    ports = fields.FileField(validators=[validators.DataRequired(message='请填写端口配置')])
    mem_limit = fields.IntegerField(validators=[validators.DataRequired(message='请填写内存容量上限')])
    database = fields.StringField(validators=[validators.DataRequired(message='请填写数据库名称')])
    charset = fields.StringField(validators=[validators.DataRequired(message='请填写字符集')])

    def validate_image_name(self, field):
        image_name = field.data
        if image_name != ImageTypeEnum.mysql.name:
            raise validators.ValidationError(f'{image_name}镜像不支持')

    def validate_name(self, field):
        name = field.data
        resource = self.resource.data

        if not resource:
            raise validators.ValidationError(f'请传入resource对象')

        container = resource.get_container(name=name)
        if container and container.status == ContainerStatusEnum.running.name:
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

            free_port = resource.get_free_port(target_port)
            if not free_port:
                raise validators.ValidationError('无可用端口, 请稍后再试')

            if free_port != target_port:
                raise validators.ValidationError(f'{target_port} 端口已被占用, 推荐使用{free_port}端口')

    def validate_charset(self, field):
        charset = field.data
        if charset not in CharsetEnum.__members__.keys():
            raise validators.ValidationError(f'{charset}字符集当前不支持')


class MysqlConfigForm(BaseForm):
    """Mysql config的form校验类"""
    name = fields.StringField(validators=[validators.DataRequired(message='请填写容器名称')])

    def validate_name(self, field):
        name = field.data
        resource = self.resource.data

        if not resource:
            raise validators.ValidationError(f'请传入resource对象')

        if not resource.get_container(name=name):
            raise validators.ValidationError(f'[{name}]容器不存在')
