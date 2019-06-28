#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo01.new_site.py 
# __date__   = 2019/6/6  13:59
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------
from kingAdmin.admin_base import BaseKingAdmin

#  注册 Admin 类
class AdminSite:
    def __init__(self):
        self.enabled_admins = {}

    def register(self,model_class, admin_class=None):
        """  注册 Admin 表  """
        print('register:',model_class,admin_class)
        app_name = model_class._meta.app_label     # 获取 app 名
        model_name = model_class._meta.model_name  # 获取 表  名

        # 为 了 避免 多个 model 共享 同一个 BaseKingAdmin 内存对象
        if not admin_class:
            admin_class = BaseKingAdmin()
        else:
            admin_class = admin_class()

        # 将 model 中的表类地址 复制给 对应的 admin 中 视图类 的 一个 类属性
        admin_class.model = model_class

        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] = {}
        self.enabled_admins[app_name][model_name] = admin_class

site = AdminSite()
