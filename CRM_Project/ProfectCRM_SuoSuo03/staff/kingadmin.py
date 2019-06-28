#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo01.kingadmin.py 
# __date__   = 2019/6/6  14:23
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------

from kingAdmin.new_site import site

from staff import models

from kingAdmin.admin_base import BaseKingAdmin

class AnimalAdmin(BaseKingAdmin):
    list_display = ['id', 'name', 'gender', 'age']

print(' Student KingAdmin ..... ')


site.register(models.Animal, AnimalAdmin)
site.register(models.Role)
site.register(models.Menus)


