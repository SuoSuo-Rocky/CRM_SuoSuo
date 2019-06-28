#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo03.permission_hook.py 
# __date__   = 2019/6/28  13:43
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------

def obj_list_filter_table(request):
    print('permission Hook is Running ...........')
    if str(request.user.id ) == request.GET.get('consultant'):
        print(' 值可以搜索 ')
    return True