# Create your views here.
from django.shortcuts import render, HttpResponse, redirect,reverse
from django.http import JsonResponse
from django.views import View
from repository.models import  *
import json

# Django 自带验证
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# 动态获取项目settings配置
from django import conf
import importlib

from kingAdmin import app_setup
app_setup.kingadmin_auto_discover()  # 全局 执行
from kingAdmin import new_site

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage

from kingAdmin.admin_base import BaseKingAdmin
from suosuo import settings

from django.db.models import Q

# 自定义 权限 装饰器
from kingAdmin.permission import check_permission
@check_permission
@login_required
def app_index(request):
    enabled_admins = new_site.site.enabled_admins
# enabled_admins= {
#                       "app_name": {
#                                   "model_name": admin_class,
#                                   "model_name": admin_class,
#                                   "model_name": admin_class},
#                      "app_name": {
#                                   "model_name": admin_class,
#                                   "model_name": admin_class,
#                                   "model_name": admin_class,
#                                   }
#                     ..........................
#                     }
    # 从 配置文件中 读取路径

    return render(request, 'kingadmin/app_index.html', {"enabled_admins": enabled_admins})
    # return HttpResponse("fdfdfdf")


# 单个 app 的首页
def one_app(request, app_name):
    enabled_admins = new_site.site.enabled_admins
    tmp_admins = {}
    for key in enabled_admins:
        if key == app_name:
            tmp_admins[key] = enabled_admins[key]
            break


    return render(request,'kingadmin/app_index.html', {"enabled_admins":tmp_admins})





#  过滤
def get_filter_result(request,querysets):
    """ 过滤 """
    filter_conditions = {}    #   用于创建 自定义标签 选定 <option> 标签
    conditions = {}           #   DB 查询条件
    for key, val in request.GET.items():
        if key in ('page', '_o', '_q'): continue
        if val != 'None':
            if key == "consultant":
                conditions[key + '__name'] = val
            elif key == "date":
                conditions[key + '__gte'] = val
            else:
                conditions[key] = val
            filter_conditions[key] = val
        else:
            filter_conditions[key] = None
    # else:
    #     conditions[key + '__name'] = val
    # print('conditions==',conditions)
    # print('filter_conditions==',filter_conditions)

    return querysets.filter(**conditions), filter_conditions

# 排序
def get_ordered_result(request,querysets,admin_class):
    """ 排序  """
    admin_class.current_ordered_key = {}
    ordered_index = request.GET.get('_o', "")
    if ordered_index:
        order_key = admin_class.list_display[abs(int(ordered_index))]
        admin_class.current_ordered_key[order_key] = ordered_index   #   保存 上次的 记录
        # admin_class.current_ordered_key = admin_class.current_ordered_key

        if ordered_index.startswith('-'):
            order_key = '-' + order_key
        return querysets.order_by(order_key)

    return querysets

def get_search_result(request,querysets,admin_class):
    query = Q()
    query.connector = "OR"
    search_key = request.GET.get('_q', '')
    if search_key:
        for field in admin_class.search_fields:
            query.children.append(("%s__contains"% field,search_key))
        return querysets.filter(query),search_key
    return querysets,search_key

# 返回到  数据   前端 ，
@check_permission
@login_required
def table_obj_list(request,app_name,model_name):
    """  取出 指定 表中的 指定页中的 数据 返回到前端  """
    #*********************         很重要        ****************************
# 疑问解析: 此 admin_class 对象只是 获取， 并不是创建 : 原因分析:
    #  服务一启动，全局变量执行完一遍存储在内存, 剩下的 就是 接受请求 和 做出响应 了。
    #  在这个响应的过程中， 需涉及到 使用全局变量的地方 ， 都是获取一下使用一下，当在处理下一次
    #  的响应的 时候还要使用到相同全局变量的话，是保存有 上一次以及更久远的时候所保存的数据的。

# 故要 分清 此对象 是否是 全局变量， 若是则可以 获取到 在之前使用相同此变量时 所存储的数据的。
    admin_class = new_site.site.enabled_admins[app_name][model_name]
    print('admin_class  ID=',id(admin_class))
    # print("app_name,model_name----->",model_name,admin_class)
    model_class = admin_class.model
    # print('model_class----->', model_class)

    # 使其 倒序， 让新添加的 数据 显示 在最上方
    if request.method == "POST":
        selected_action = request.POST.get("action")
        selected_ids = json.loads(request.POST.get("selected_ids"))
        print(selected_action,"////////\n",selected_ids)
        selected_func = getattr(admin_class, selected_action)
        selected_func(request, selected_ids, admin_class)

        # return selected_func(request,selected_ids,admin_class)


    querysets = model_class.objects.all().order_by('-id')


    # print("-------------------->")
    for key,val in request.GET.items():
        print('key=', key, '\t; val=', val)
    #
#  过滤
        # 根据 request 对象 获取过滤选项并保存在 admin_class 中，构造有效的 过滤条件，Query DB ，
    querysets, filter_conditions = get_filter_result(request, querysets)
    admin_class.filter_conditions = filter_conditions

# 搜索 ：  基于 过滤 之后
    querysets, search_key = get_search_result(request, querysets, admin_class)
    admin_class.search_key = search_key

    #例: filter_conditions= {'name': '老铁', 'contact': '124564515', 'status': '2'}
    # print('filter_conditions=',filter_conditions)
    # print('QuerySets------>',querysets)
# 排序
        # 根据 request 对象 获取在 list_display 中所要排序的表字段  下标， Update DB
    querysets= get_ordered_result(request, querysets, admin_class)

# 分页
    admin_class.current_page_num = {}
    p = Paginator(querysets,settings.page_data_num)
    page = request.GET.get("page")
    try:
        querysets = p.page(page)
        admin_class.current_page_num["page"] = page        #  保存 page : 当前分页数
    except PageNotAnInteger:
        querysets = p.page(1)                              # 当 url 中 无 page 参数时执行
    except EmptyPage:
        querysets = p.page(p.num_pages)

    return render(request, 'kingadmin/table_obj_list.html', {
        "querysets": querysets,
        "admin_class": admin_class,
        "model_name": model_name,
        'app_name': app_name,
    })
    # return HttpResponse("ok")

# 数据详情页 修改数据
@login_required
def table_obj_change(request, app_name, model_name, obj_id):
    """  表记录详情页 修改数据  """
# Django 的 静态 form
    # from kingAdmin import forms
    # form = forms.CustomerForm()
# 动态 form
    from kingAdmin.dynamic_forms import create_dynamic_model_form
    admin_class = new_site.site.enabled_admins[app_name][model_name]

    model_form = create_dynamic_model_form(admin_class)
    row_obj = admin_class.model.objects.get(id = obj_id)
    many_to_many_fields = []

    # 获得 此 表中的 所有 many_to_many 字段，默认 在添加数据 和修改 数据 时 显示为左右两边的 select 框
    for item in admin_class.model._meta.get_fields():
        if item.get_internal_type() == "ManyToManyField":
            many_to_many_fields.append(item.name)
    admin_class.filter_horizontal = list(admin_class.filter_horizontal)
    admin_class.filter_horizontal.extend(many_to_many_fields)

    if request.method == "GET":
        form_obj = model_form(instance = row_obj)
    elif request.method == "POST":
        form_obj = model_form(instance = row_obj, data = request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(to='/kingadmin/%s/%s/'% (app_name,model_name))

    return render(request, 'kingadmin/table_obj_change.html',locals())

@login_required
def table_obj_delete(request, app_name, model_name, obj_id):
    from kingAdmin.dynamic_forms import create_dynamic_model_form
    admin_class = new_site.site.enabled_admins[app_name][model_name]
    row_obj = admin_class.model.objects.get(id=obj_id)

    return render(request, 'kingadmin/table_obj_delete.html', locals())


def table_obj_add(request, app_name, model_name):

    from kingAdmin.dynamic_forms import create_dynamic_model_form
    admin_class = new_site.site.enabled_admins[app_name][model_name]

    model_form = create_dynamic_model_form(admin_class, form_add=True)

    many_to_many_fields = []
    # 获得 此 表中的 所有 many_to_many 字段，默认 在添加数据 和修改 数据 时 显示为左右两边的 select 框
    for item in admin_class.model._meta.get_fields():
        if item.get_internal_type() == "ManyToManyField":
            many_to_many_fields.append(item.name)
    admin_class.filter_horizontal = list(admin_class.filter_horizontal)
    admin_class.filter_horizontal.extend(many_to_many_fields)


    if request.method == "GET":
        form_obj = model_form()
    if request.method == "POST":
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(to='/kingadmin/%s/%s/' % (app_name, model_name))

    return render(request,'kingadmin/table_obj_add.html', locals())


class acc_login(View):
    error_msg = ''
    def get(self, request, *args, **kwargs):
        return render(request, 'kingadmin/login.html',locals())

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
            login(request,user)
            # 登录成功的情况下 跳转到 初次 请求的页面
            return redirect(request.GET.get('next', '/kingadmin'))
        else:
            # 设置 错误提示消息
            error_msg = 'Wrong username or password! '

        print('username=',username,'\n password=',password,'\nuser=',user)
        # 在前端页面 使用 模板 语言 可以直接 调用 request  对象，
        # 在 后台若验证成功自动 封装 user  到 request 中
        return render(request, 'kingadmin/login.html', {'error_msg': error_msg})
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
