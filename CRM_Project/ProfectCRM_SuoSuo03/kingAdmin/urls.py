#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo01.urls.py 
# __date__   = 2019/6/6  11:29
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------

from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from kingAdmin import views


urlpatterns = [
    url(r'^$', views.app_index, name='backend_page'),
    url(r'^(\w+)/$', views.one_app, name="app_page"),
    url(r'^(?P<app_name>\w+)/(?P<model_name>\w+)/$', views.table_obj_list, name="table_obj_list"),
#  需要 添加 正则 的 开头 字符
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_obj_change, name="table_obj_change"),
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.table_obj_delete, name="table_obj_delete"),
    url(r'^(\w+)/(\w+)/add/$', views.table_obj_add, name="table_obj_add"),
    path('login', views.acc_login.as_view(), name="login"),  # 每次写 CBV 时 ， 就忘了 调用 as_view()
    url('^logout$', views.acc_logout, name='logout'),
]
