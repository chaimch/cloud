from wtforms import fields
from wtforms import validators

from const.enum import ImageType
from exts.cloudform import BaseForm


class MysqlInstanceForm(BaseForm):
    """mysql instance的form校验类"""
    image_name = fields.StringField(validators=[validators.DataRequired(message='请填写镜像名称')])
    name = fields.StringField(validators=[validators.DataRequired(message='请填写容器名称')])
    ports = fields.FileField(validators=[validators.DataRequired(message='请填写端口配置')])
    mem_limit = fields.IntegerField(validators=[validators.DataRequired(message='请填写内存容量上限')])

    def validate_image_name(self, field):
        image_name = field.data
        if image_name != ImageType.mysql.name:
            raise validators.ValidationError(f'{image_name}镜像不支持')


class MysqlConfigForm(BaseForm):
    """mysql config的form校验类"""
    name = fields.StringField(validators=[validators.DataRequired(message='请填写容器名称')])
