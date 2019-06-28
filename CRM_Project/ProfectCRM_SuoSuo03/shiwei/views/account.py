#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __date__   = 2019/5/8  10:25
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views import View
from repository.models import  *
import json
import os
from django import conf
from django.views.decorators.csrf import csrf_exempt
# 设置 没登录成功 ， 则跳转到 登录页面
#  登录失败的情况下访问 ：
            #    http://192.168.0.104:9999/accounts/login/?next=/shiwei/
from django.contrib.auth.decorators import login_required

from shiwei.forms import EnrollmentForm
from django.utils.timezone import datetime

# 自定义权限
from kingAdmin.permission import check_permission

@check_permission
@login_required   # 登录失败 ， 则在 settings 中配置
def dashboard(request):



    return render(request, 'shiwei/dashboard.html',)


@login_required
def table_obj_list(request,app_name,model_name):
    """  取出 指定 表中的数据 返回 到前端  """
    pass

@login_required
def stu_enrollment(request):

    customers = CustomerInfo.objects.all()
    class_lists = ClassList.objects.all()
    if request.method == "POST":
        customer_id = request.POST.get("customer")
        banji_id = request.POST.get('banji')
        try:
            enrollment_obj = StudentEnrollment.objects.create(
                customer_id = customer_id,
                class_grade_id = banji_id,
                consultant_id = request.user.userprofile.id
            )
            # enrollment_link = "http://localhost:8524/enrollment/%s/"%enrollment_obj.id
        except Exception as e:
            error_message = "你已报名此班级，请选择其他班级......... "

    return render(request, 'shiwei/stu_enrollment.html', locals())


def enrollment(request, enrollment_id):
    """  学员在线报名表   """
    # request.session[enrollent]
    enrollment_obj = StudentEnrollment.objects.get(id=enrollment_id)
    if enrollment_obj.contract_agreed == True:
        return HttpResponse("报名合同正在 审核中 ........")
    # enrollment_obj.customer : 一个 类 CustomerInfo 的 实例， 不是一个  QuerySet
    customer_form = EnrollmentForm(instance=enrollment_obj.customer)
    if request.method == 'POST':
        customer_form = EnrollmentForm(instance=enrollment_obj.customer, data=request.POST)
        enabled_field = ('name', 'id_num', 'sex', 'emergency_contact')
        effective_data = {}
        if customer_form.is_valid():
            customer_form.save()
            # for field in customer_form.cleaned_data:
            #     if field in enabled_field:
            #         effective_data[field] = customer_form.cleaned_data[field]
            # customer_form.instance : 一个 类 CustomerInfo 的 实例， 不是一个  QuerySet
            #   ORM 的 update 方法 是对 QuerySet 集合 的 更新操作， 单个对象没有 更新操作。
            # enrollment_obj.customer.__class__.objects.filter(id=customer_form.instance.id).update(**effective_data)
            # print('class===', type(customer_form.instance))
            # print('enrollment_obj.customer', type(enrollment_obj.customer))
            # print('ID ======',customer_form.instance.id)
            #
            # print('clean_data===',customer_form.cleaned_data)
            # print('customer---------》error', customer_form.errors)
            return redirect(to='/shiwei/enrollment/%s/contract_upload'%enrollment_id)
        else:
            #  犯得 错误 之一， 验证失败 之后 要把 提交的 返回到前端， 保留之前编辑的数据
            customer_form = EnrollmentForm(instance=enrollment_obj.customer, data=request.POST)

    return render(request,'shiwei/enrollment.html', locals())


def contract_upload(request, enrollment_id):
    # 列出 所有 文件
    enrollment_obj = StudentEnrollment.objects.get(id=enrollment_id)
    upload_files = []
    enrollment_upload_dir = os.path.join(conf.settings.UPLOAD_FILES_DIR, enrollment_id)
    if os.path.isdir(enrollment_upload_dir):
        upload_files = os.listdir(enrollment_upload_dir)
    if request.method == "POST":
        print('POST------->', request.POST)
        return HttpResponse("passed")
    enrollment_obj.contract_agreed = True
    print('all file = ',upload_files)
    return render(request, 'shiwei/contract_upload.html', locals())






@csrf_exempt
def enrollment_fileupload(request, enrollment_id):
    charge = os.path.isdir(os.path.join(conf.settings.UPLOAD_FILES_DIR, enrollment_id))
    addr = os.path.join(conf.settings.UPLOAD_FILES_DIR, enrollment_id)
    if not charge:
        os.mkdir(addr)
    file_obj = request.FILES.get('file')
    file_name = os.path.join(addr, file_obj.name)
    if len(os.listdir(addr)) <= 2:
        with open(file_name, 'wb') as f:
            for chunks in file_obj.chunks():
                f.write(chunks)
    else:
        return HttpResponse(json.dumps({"status": False, 'err_msg': 'max file num is 2'}))

    return HttpResponse(json.dumps({"status": True}))



def wanganshi(request):
    return HttpResponse("OK")















