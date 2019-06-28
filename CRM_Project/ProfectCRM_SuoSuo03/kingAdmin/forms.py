#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo03.forms.py 
# __date__   = 2019/6/12  10:32
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------

from django.forms import ModelForm

from repository.models import *

# 添加  静态 的  Django 的  ModelForm
class CustomerForm(ModelForm):
    class Meta:
        model =  CustomerInfo
        # fields = ['name', 'consultant', 'status']
        fields = "__all__"    #  添加 所有的 字段
    def __new__(cls, *args, **kwargs):
        print("__new__",cls,args,kwargs)
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class': 'form-control'})
        return ModelForm.__new__(cls)

def create_dynamic_model_form(admin_class):
    """  动态的 生成  modelForm  """
    class Meta:
        model =  CustomerInfo
        # fields = ['name', 'consultant', 'status']
        fields = "__all__"    #  添加 所有的 字段
    dynamic_form = type('DynamicModelForm', (ModelForm,), {"Meta": Meta})
    print()




