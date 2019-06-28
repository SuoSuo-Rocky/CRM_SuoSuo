#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo03.permission_list.py 
# __date__   = 2019/6/19  19:20
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------

# 注意 ： 字典元素的书写格式为:

"""
:key 为 model.py 文件中 permission 元祖中的元素的 键，第一个 单词为 app 名
:value [
            url的别名，
            请求方法，
            url 正则匹配参数
            url 正则匹配分组 参数 键值对 匹配
            url锚参, 键 存在，
            url锚参数键和值 匹配，
            自定义钩子方法
        ]
"""



perm_dic = {
    "repository_backend_page": ["backend_page", 'GET', [], {}, [], {}],  # 可查看到 所有 app 中的 数据表
    "repository_app_page": ['app_page', 'GET', [], {}, [], {}], # 查看 某一个 app 中 数据表
    "repository_table_obj_list": ['table_obj_list', 'GET', [], {}, [], {}], # 进入 某张 数据表的 首页
}