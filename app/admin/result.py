# -*- coding: utf-8 -*-
# @Time   : 2019/4/13 13:25
# @Author : Flouis
from enum import Enum


# 通用返回类
class Result:
    code = 0        # 结果码
    msg = ""        # 通知消息
    data = None     # 交互数据

    def __init__(self, code, msg, data):
        self.code = code
        self.msg = msg
        self.data = data


# 结果枚举类
class ResultEnum(Enum):
    SUCCESS = Result(200, "请求成功", None)
    FAIL = Result(400, "请求失败", None)

    @staticmethod
    def obj2json(obj):
        return {
            "code": obj.code,
            "msg": obj.msg,
            "data": obj.msg
        }


# print(ResultEnum.obj2json(ResultEnum.SUCCESS.value))


