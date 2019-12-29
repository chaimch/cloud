from enum import Enum


class StrEnum(str, Enum):
    pass


class IntEnum(int, Enum):
    pass


class DictEnum(dict, Enum):
    pass


class ResponseCodeEnum(IntEnum):
    """响应枚举"""
    ok = 0
    wrong_args = 102
    db_not_update = 201
    inner_error = 501


class ResponseMsgEnum(StrEnum):
    """响应提示信息"""
    ok = 'ok'
    wrong_args = '参数有误'
    db_not_update = '数据未更新'
    inner_error = '内部出错'


class ImageTypeEnum(StrEnum):
    redis = 'redis'
    mysql = 'mysql'


class ContainerStatusEnum(StrEnum):
    created = '已创建'
    running = '正在运行'
    exited = '已退出'


class CharsetEnum(StrEnum):
    utf8 = 'utf8'
    utf8mb4 = 'utf8mb4'
