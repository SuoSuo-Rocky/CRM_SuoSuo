#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo01.app_setup.py 
# __date__   = 2019/6/6  14:14
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------

import importlib
from django import conf

def kingadmin_auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        # 动态 导入文件  第  一  种方案:
        # __import__("%s.kingadmin"%app_name)
        try:
        # 动态 导入文件  第  二  种方案:
            moudel = importlib.import_module('.kingadmin', app_name)
            print('moudel-----> ',moudel)
        except Exception:
            pass