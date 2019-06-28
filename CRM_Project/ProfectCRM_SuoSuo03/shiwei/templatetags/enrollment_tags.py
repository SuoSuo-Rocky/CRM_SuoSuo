#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo03.enrollment_tags.py 
# __date__   = 2019/6/16  9:46
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------
import datetime
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def get_path(enrollment_obj):
    ele = """<a href="http://192.168.0.104:8888/shiwei/enrollment/%s/">http://localhost:8888/shiwei/enrollment/%s/</a>""" %(enrollment_obj.id, enrollment_obj.id)
    return mark_safe(ele)