#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo01.admin_base.py 
# __date__   = 2019/6/6  17:00
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------
from django.shortcuts import render

class BaseKingAdmin:
    def __init__(self):
        self.actions = []  # 避免 同一 BaseKingAdmin 对象 多次 extend
        self.actions.extend(self.default_actions)
        print('BaseKingAdmin----->action==', self.actions)

    list_display = []
    list_filter = []
    search_fields = []
    readonly_fields = []
    filter_horizontal = []
    default_actions = ['delete_selected_objs', ]

    def delete_selected_objs(self, request, selected_ids, admin_class):
        objs = admin_class.model.objects.filter(id__in=selected_ids).delete()
        # model_name = admin_class.model._meta.model_name
        # querysets.delete()
        # return render(request, 'kingadmin/table_obj_delete.html', locals())







