#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo03.forms.py 
# __date__   = 2019/6/15  16:41
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------


from repository import models
from django.forms import ModelForm
from django import forms
#
class EnrollmentForm(ModelForm):
    class Meta:
        model = models.CustomerInfo
        fields = "__all__"
        exclude = ['consult_content', 'status', 'consult_courses', 'source', 'contact_type']    # 不显示
        readonly_fields = ('contact', 'consultant', 'referral_from')

    def __new__(cls, *args, **kwargs):
        print("__new__",cls,args,kwargs)
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            #  不可 编辑
            if field_name in cls.Meta.readonly_fields:
                field_obj.widget.attrs.update({'class': 'form-control', 'disabled': 'disabled',})
                continue
            field_obj.widget.attrs.update({'class': 'form-control'})
        return ModelForm.__new__(cls)


    def clean(self):
        """  全局 的 ModelForm  Hook 函数 """
        print('All Field ---->', self.base_fields)
        print('clean Func---->', self.cleaned_data)
        if self.errors:
            raise forms.ValidationError("Please fix errors before re_submit .....")
        if self.instance.id is not None:
            # 保证 只读的字段 不可修改， 其他的字段不可为空
            for field in list(self.cleaned_data.keys()):

                if field in self.Meta.readonly_fields:
                    old_field_val = getattr(self.instance, field)
                    form_val = self.cleaned_data.get(field)
                    #  添加  单个字段 的 错误
                    if old_field_val != form_val:
                        self.add_error(field, "ReadOnly Field: field should be '{value}', not '{new_value}' ".\
                                       format(value=old_field_val, new_value = form_val))
                        break
                if field == 'sex':
                    if self.cleaned_data.get(field) not in [0, 1]:
                        self.add_error(field, 'Field is required: %s'% field)
                        break
                elif not self.cleaned_data.get(field):
                    self.add_error(field, "Field is required: %s"% field)
                    break
        print("Error is ---->", self.errors)  #  全局的 错误

        return self.cleaned_data

















