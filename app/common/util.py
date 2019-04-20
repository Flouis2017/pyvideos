# -*- coding: utf-8 -*-
# @Time   : 2019/4/13 15:35
# @Author : Flouis
# @Desc : ==============================================
# I make my dream come true by code.
# ======================================================
from sqlalchemy import text
from app import db
import re


# 自定义sql工具类，用于执行原生sql，将查询结果封装成[{}]
class SqlUtil:

    # 获取column_names:
    @staticmethod
    def get_column_names(sql):
        regex = r"AS\s+[\w]+|aS\s+[\w]+|As\s+[\w]+|as\s+[\w]+"
        res = re.findall(regex, sql)
        for i in range(0, len(res)):
            res[i] = res[i][3:].strip()
        return res

    # 元组转字典
    @staticmethod
    def tuple_to_dict(column_names, tuple_data):
        if len(tuple_data) != len(column_names):
            raise Exception('Error may occurred by sql with no "As" ')
        return dict(zip(column_names, tuple_data))

    @staticmethod
    def exe_sql(sql, param):
        _list = []
        if param:
            res = db.session.execute(text(sql), param).fetchall()
        else:
            res = db.session.execute(text(sql)).fetchall()
        column_names = SqlUtil.get_column_names(sql)
        for row in res:
            _list.append(SqlUtil.tuple_to_dict(column_names, row))
        return _list


