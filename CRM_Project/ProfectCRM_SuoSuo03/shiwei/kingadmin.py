#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo01.kingadmin.py 
# __date__   = 2019/6/6  12:35
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------

from kingAdmin.new_site import site
from repository import models
from kingAdmin.admin_base import BaseKingAdmin
print(' Shiwei  CRM  Admin......   ')

class CustomerAdmin(BaseKingAdmin):
    list_display = ('id', 'name', 'contact_type', 'contact', 'source', 'referral_from', 'consult_content', 'consultant', 'status',)
    list_editable = ('name', 'contact_type', 'contact', 'source', 'referral_from', 'consultant', 'status',)
    list_filter = ['name', 'contact','status','contact_type','source','consultant', 'date']
    search_fields = ("name", "consult_content")
    readonly_fields = ['status', 'contact', ]
    filter_horizontal = ('consult_courses',)   # 配置 显示 为 左右 两边的 select 框 ，many_to_many 字段 自动此样式
    actions = ['change_status', ]
    def change_status(self,request,querysets):
        querysets.update(status=0)
        # print('querysets=',querysets)


class userprofileView(BaseKingAdmin):
    list_display = ('id', 'name','password',)
    list_editable = ('name', )
    list_filter = ('name',)
    filter_horizontal = ('role',)
    list_display_links = ('id',)
    actions = []

class roleView(BaseKingAdmin):
    list_display = ('id', 'name',)
    # 主键字段 不可 位于 list_editable 中， 主键 不可编辑
    list_editable = ('name',)
    list_display_links = ('id',)
    actions = []

site.register(models.CustomerInfo,CustomerAdmin)
site.register(models.UserProfile,userprofileView)
site.register(models.ClassList)
site.register(models.Course)
site.register(models.CourseRecord)
site.register(models.Student)
site.register(models.StudyRecord)
site.register(models.CustomerFollowUp)
site.register(models.Role, roleView)
site.register(models.Menus)
site.register(models.Branch)





