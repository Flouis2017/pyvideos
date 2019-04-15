# -*- coding: utf-8 -*-
# @Time   : 2019/4/13 15:35
# @Author : Flouis
# @Desc : ==============================================
# I make my dream come true by code.
# ======================================================


# 自定义sql工具类，用于执行原生sql，将查询结果封装成[{}]
class SqlUtil:

    # 元组转字典
    @staticmethod
    def tuple_to_dict(self, data, column_names):
        return dict(zip(column_names, data))




