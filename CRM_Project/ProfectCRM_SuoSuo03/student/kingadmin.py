#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo01.kingadmin.py 
# __date__   = 2019/6/6  14:23
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------

from kingAdmin.new_site import site

from student import models

from kingAdmin.admin_base import BaseKingAdmin

print(' Student KingAdmin ..... ')

class TestAdmin(BaseKingAdmin):
    list_display = ['id', 'name',]


site.register(models.test,TestAdmin)


