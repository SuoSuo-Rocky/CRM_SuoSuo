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
# class CustomerForm(ModelForm):
#     class Meta:
#         model =  CustomerInfo
#         # fields = ['name', 'consultant', 'status']
#         fields = "__all__"    #  添加 所有的 字段

def create_dynamic_model_form(admin_class, form_add=False):
    """  动态的 生成  modelForm
            form_add 默认 时 修改 的 表单，True 时 为新增

    """
    class Meta:
        model =  admin_class.model

        # fields = ['name', 'consultant', 'status']
        fields = "__all__"    #  添加 所有的 字段
        if not form_add:  # 修改
            exclude = admin_class.readonly_fields
        #  在服务 运行状态中 自始至终 admin_class 都为 一个 对象，
            admin_class.form_add = False
        else:  # 增加
            admin_class.form_add = True

    def __new__(cls, *args, **kwargs):
        print("__new__", cls, args, kwargs)
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class': 'form-control'})

            # 让 只读  的 字段为 disabled 方案 不可行
            # if field_name in admin_class.readonly_fields:
            #     field_obj.widget.attrs.update({'class': 'form-control', 'disabled': "disabled"})


        return ModelForm.__new__(cls)

    dynamic_form = type('DynamicModelForm', (ModelForm,), {"Meta": Meta, '__new__': __new__})
    # print("dynamic_form= ",dynamic_form)
    return dynamic_form




