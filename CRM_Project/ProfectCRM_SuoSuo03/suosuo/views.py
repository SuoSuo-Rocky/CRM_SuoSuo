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

# Django 自带验证
from django.contrib.auth import authenticate,login,logout


#
class acc_login(View):
    error_msg = ''
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html',locals())
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
  # 第一步: 验证
        # 结果 为 从 DB 中 取出 的 user 对象，只是 单纯的 判断 数据 是否正确
        user = authenticate(username = username, password = password)
        if user:
            print("passed authentication ", user)
 # 第二步: 真正的 登录，生成 session
            # 自动 将  user 对象保存到 session 中 ， request.user = user
            login(request, user)
            # 登录成功的情况下 跳转到 初次 请求的页面
            return redirect(request.GET.get('next','/shiwei'))
        else:
            # 设置 错误提示消息
            error_msg = 'Wrong username or password! '

        print('username=',username,'\n password=',password,'\nuser=',user)
        # 在前端页面 使用 模板 语言 可以直接 调用 request  对象，
        # 在 后台若验证成功自动 封装 user  到 request 中
        return render(request, 'login.html', {'error_msg': error_msg})
        #  要加 斜杠   否则 报错
        # return redirect('/shiwei')
###############    或者 FBV  的 方式
# def login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         print('username=',username,'\n password=',password)
#     return render(request, 'login.html',locals())

def acc_logout(request):
    logout(request)   # 退出， 清空 session
    return redirect('/login')


def popup(request):

    return render(request, 'my_popup.html',locals())


def tab(request):

    return render(request, 'tab_plugins.html', locals())















