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


class ResponseMsgEnum(StrEnum):
    """响应提示信息"""
    ok = 'ok'
    wrong_args = '参数有误'
    db_not_update = '数据未更新'
