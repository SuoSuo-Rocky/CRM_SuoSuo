#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo01.urls.py 
# __date__   = 2019/6/5  14:53
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include

from shiwei.views import account

urlpatterns = [
    path('wanganshi', account.wanganshi, name="wanganshi"),
    path('', account.dashboard, name='sales_dashboard'),
    path('stu_enrollment/', account.stu_enrollment, name='stu_enrollment'),
    url(r'^enrollment/(\d+)/$', account.enrollment, name='enrollment'),
    url(r'^enrollment/(\d+)/contract_upload$', account.contract_upload, name='contract_upload'),
    url(r'^enrollment/(\d+)/fileupload/$', account.enrollment_fileupload, name='enrollment_fileupload'),

    # path('sales_dashboard', account),
]
