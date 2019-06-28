#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# __name__   = ProfectCRM_SuoSuo01.kingadmin_tags.py 
# __date__   = 2019/6/6  19:15
# __author__ ='Shi Wei'
# __description__: 
# --------------------------------------------------------------
from django.template import Library
from django.utils.safestring import mark_safe
register = Library()
import time,datetime
from suosuo import settings


# 过滤 select  标签的 创建
@register.simple_tag
def column_format(filter_column_name,admin_class):
    """ 生成 过滤 的 select 标签  """
    # 通过 admin 对象 的 model 属性 获取 model 对象
    model_class = admin_class.model
    # 列对象， 就是 字段 对象 ，对应 models.py 中 表类中的 一个 属性
    column_obj = model_class._meta.get_field(filter_column_name)
    # 获取 此字段对象 的 choices 属性， 没有的话 则为 一个 空列表 []
    column_choices = column_obj.choices
    # 判断 此字段对象 是否为 关联对象 ，不关联表的话 则为空， 布尔值 为 False
    related_model = column_obj.related_model
    # 获取 此字段对象的 的 内部的 models.Field 类型对象， 例如: CharField , DateField 等
    internal_type = column_obj.get_internal_type

    column_name = "<span>%s</span>"% filter_column_name
    column_format = "%s<select class='' name='%s'>"% (column_name, filter_column_name)
    option = "<option value='None'>--- All ---</option>"
    column_format += option
    # 从 后台中 获取 过滤选项， 包括 值为 None 的， 因为我要根据 键 创建 select 标签，返回前端显示
    filter_conditions = admin_class.filter_conditions


    # print("tag------>filter_column_name=",filter_column_name)
    # print("tag------->filter_conditions",filter_conditions)
    if column_obj.get_internal_type() in ('DateField', 'DateTimeField'):
        time_obj = datetime.datetime.now()
        time_list = [
            [time_obj, 'Today'],
            [time_obj - datetime.timedelta(7), '七天内'],
            [time_obj.replace(day=1), '本月'],
            [time_obj - datetime.timedelta(90), '三个月内'],
            [time_obj.replace(month=1, day=1), 'YearToDay(YTD)'],
        ]
        for i in time_list:
            selected = ''
            time_to_str = '' if not i[0] else "%s-%s-%s"%(i[0].year,i[0].month,i[0].day)
            try:
                if time_to_str == admin_class.filter_conditions.get(filter_column_name):
                    selected = "selected"
            except Exception as e:
                pass
            option = "<option value='%s' %s>%s</option>" % \
                     (time_to_str, selected, i[1])
            column_format += option
    elif column_choices:
        # print("--------------->",type(filter_conditions[filter_column_name]))
        for choice in column_choices:
            # print("------------>choices",type(choice[0]))
            selected = ''
            try:
                if filter_conditions[filter_column_name] == str(choice[0]):
                    selected = 'selected'
            except Exception as e:
                pass
            option = "<option value='%s' %s>%s</option>"% (choice[0],selected,choice[1])
            column_format += option
        column_format += "</select>"
    else:
        if not bool(related_model):
            # if related_model == "ForeignKey":
            data = list(model_class.objects.all().values(filter_column_name))
            end_data = []
            for k,v in enumerate(data): # 例: v = {"name": "老铁"}
                item = (k,v[filter_column_name])
                end_data.append(item)

            for choice in end_data:
                selected = ''
                try:
                    if filter_conditions[filter_column_name] == choice[1]:
                        selected = 'selected'
                except Exception as e:
                    pass
                option = "<option value='%s' %s>%s</option>"% (choice[1],selected,choice[1])
                column_format += option
        else:
            end_data = related_model.objects.all().values_list("name")
            for item in end_data:
                selected = ""
                try:
                    if filter_conditions[filter_column_name] == item[0]:
                        selected = "selected"
                except Exception as e:
                    pass
#  print("foreign----------------------->")
                option = "<option value='%s' %s>%s</option>" % (item[0], selected, item[0])
                column_format += option

        column_format += "</select>"

    return mark_safe(column_format)

#  返回到 前端 过滤 的  URL
@register.simple_tag
def get_filter_url(admin_class, render_html=True):
    """ 获得 过滤 的  URL  """
    ele = ''
    if admin_class.filter_conditions:
        for k,v in admin_class.filter_conditions.items():
           ele += '&%s=%s' %(k, v)
        if render_html:
            # 用于返回前端 渲染页面
            return mark_safe(ele)
        else:
            # 用于 让别的方法调用，获得 过滤的 URL
            return ele
    return ''

#  获取 排序的 URL
def get_sorted_url(admin_class):
    """  获取 排序的 URL """
    ele = ''
    if admin_class.current_ordered_key:  # 例如: {"name": -1}
        ele = "&_o=%s"% list(admin_class.current_ordered_key.values())[0]
        return mark_safe(ele)
    return ''

#  返回到前端 分页 的 URL
@register.simple_tag
def get_page_url(admin_class):
    """  返回到前端 分页 的 URL """
    ele = ''
    if admin_class.current_page_num:
        ele = "&page=%s" % list(admin_class.current_page_num.values())[0]
        return mark_safe(ele)
    return ''

# 过滤 时保存 分页 的 页数，不合理，故此 方法 没有 引用
@register.simple_tag
def filter_get_page_url(admin_class):
    if admin_class.current_page_num:
        page_num = list(admin_class.current_page_num.values())[0]
        return mark_safe(page_num)
    return ''

# 过滤 时 保存 排序 分页 的 页数
@register.simple_tag
def filter_get_sorted_url(admin_class):
    #  或使用 三元 运算符 ： 一行 解决 哦！
    # return  list(admin_class.current_ordered_key.values())[0] if admin_class.current_ordered_key else ''
    if admin_class.current_ordered_key:
        sorted_num = list(admin_class.current_ordered_key.values())[0]
        return mark_safe(sorted_num)
    return ''

# 生成 表记录 数据的  <tr>
@register.simple_tag
def build_table_row(obj,admin_class):
    """  生成 一条 表记录数据 的 table element  is <tr>
    :param
        obj: querySet 集合元素 ，表的一条记录对象

    """
    ele = '<tr>'
    # 添加 一个 th  为 CheckBox, 套路 ， 添加 自定义 属性 row-select ，方便查找
    ele += """<td><input row-select="true" type="checkbox" value="%s"></td>""" % obj.id
    if hasattr(admin_class, "list_display") and admin_class.list_display:
        for column_name in admin_class.list_display:
            column_obj = admin_class.model._meta.get_field(column_name)
            # 判断  此记录的 此个 字段 是否 有 choices  属性
            if column_obj.choices:
                # 获取 此 一条记录数据 对象 当前 choices 的 选定值
                column_data = getattr(obj,'get_%s_display'% column_name)()
            else:
                # 获取 此记录 当前 字段的 值
                column_data = getattr(obj,column_name)
            # 判断 此记录  的 此个 字段 是否为 主键 字段
            if column_obj.primary_key:
                td_ele = "<td><a href='%s/change/'>%s</a></td>" % (getattr(obj,column_name),column_data)
            else:
                td_ele = "<td>%s</td>"% column_data
            ele += td_ele
    else:
        #  添加 进入 表记录修改详情页  的 URL
        td_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.pk, obj)
        ele += td_ele
    ele += '</tr>'
    return mark_safe(ele)

# 自定义 分页 标签， NB 插件， 自写 的 哦！
@register.simple_tag
def auto_page_li(request, querysets, admin_class):
    """  生成 分页 器   """
    try:
        cur_page = int(request.GET.get('page'))
    except Exception  as e:
        cur_page = 1
    # print('cur_page=',cur_page,'type=',type(cur_page))
    page_format = """<nav aria-label="..." style="" >
                        <ul class="pagination center" >
      """
    print('querysets=', querysets)
    page_num = len(querysets.paginator.page_range)
    loop = settings.html_page_num
    mid = settings.html_page_num // 2
    remainder = settings.html_page_num % 2
    left = 1
    # 获取 过滤的 URL
    filter_url= get_filter_url(admin_class, False)

    # 获取 排序的 URL
    sorted_url = get_sorted_url(admin_class)

    if querysets.has_previous():
        start_li = ("",querysets.previous_page_number())
    else:
        start_li = ("disabled",1)

    if querysets.has_next():
        end_li = ("",querysets.next_page_number())
    else:
        end_li = ("disabled",page_num)
    page_format += """<li class="%s"><a href="?page=%s%s%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>"""% (*start_li, filter_url,sorted_url)

    if len(querysets.paginator.page_range) <= settings.html_page_num:
        range_page = querysets.paginator.page_range
    else:
        if cur_page <= mid:
            left = 1
        elif cur_page >=  page_num - mid + 1:
            left = page_num - loop + 1
        else:
            if remainder == 0:
                left = cur_page - mid + 1
            else:
                left = cur_page - mid
        range_page = range(left, left + loop)
    for i in range_page:
        if cur_page == i:
            page_format += """<li class="active"><a href="?page=%s%s%s">%s<span class="sr-only">(current)</span></a></li>"""%(i, filter_url, sorted_url, i)
        else:
            page_format += """<li><a href="?page=%s%s%s">%s<span class="sr-only">(current)</span></a></li>"""%(i, filter_url, sorted_url, i)

    page_format += """<li class="%s"><a href="?page=%s%s%s" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>"""% (*end_li, filter_url, sorted_url)
    page_format += """</ul></nav>"""

    return mark_safe(page_format)

# 构造 排序 所使用的到 的 href 属性
@register.simple_tag
def get_sorted_column(column, forloop, admin_class):
    """ 用于排序，构造列名 所在的  a 标签 的 href 属性 ，返回 一个 数字，正负 代表 正逆 序 """
    current_ordered_key = admin_class.current_ordered_key
    if column in current_ordered_key:
        data = current_ordered_key[column]
        if data == '0':
            return mark_safe('-' + data)
        return mark_safe(str(int(data) * -1))
    return forloop

# 生成 排序 所使用 到的 图标
@register.simple_tag
def render_sorted_arrow(column, admin_class):
    """ 生成 列名排序 时左边 显示的 小图标  """
    current_ordered_key = admin_class.current_ordered_key
    if column in current_ordered_key:
        if current_ordered_key[column].startswith('-'):
            arrow_direction = 'bottom'
        else:
            arrow_direction = 'top'
        ele = '''<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>''' % arrow_direction
        return mark_safe(ele)
    return ''

@register.simple_tag
def show_condition(admin_class):
    ele = '搜: '
    for i in admin_class.search_fields:
      ele += i + '/ '
    return mark_safe(ele)

# 返回 model_name
@register.simple_tag
def get_model_name(admin_class):
    name = admin_class.model._meta.model_name.upper()
    return mark_safe(name)

# 返回  只读 字段的 值
@register.simple_tag
def get_obj_field_val(form_obj, field):
    """  返回  只读 字段的 值 """
    return  getattr(form_obj.instance,field)


#  返回的 是 m2m  字段关联表的 所有数据
@register.simple_tag
def get_available_m2m_data(field_name, admin_class, form_obj):
    """  返回的 是 m2m  字段所  关联的  表的 所有数据  """
    field_obj = admin_class.model._meta.get_field(field_name)
    all_data = set(field_obj.related_model.objects.all())

    print("all_date----------->", all_data)
    print('field_name----------->', field_name)
    print('admin_class----------->', admin_class)
    # print('form_obj------------->', form_obj.instance)

    # In[30]: form_obj.instance
    # Out[30]: < CustomerInfo: queue >
    if form_obj.instance.id:
        selected_data = set(getattr(form_obj.instance, field_name).all())
        return all_data.difference(selected_data)
    else:
        return all_data
    # print('selected_data-------->',selected_data)
    # return ''


# 返回的 是 m2m  字段 已选数据
@register.simple_tag
def get_selected_m2m_data(field_name, admin_class, form_obj):
    """  返回的 是 m2m  字段 已选数据  """
    if form_obj.instance.id:
        selected_data = getattr(form_obj.instance, field_name).all()
        return selected_data
    else:
        return []


# 展示 所有 于此条 数据 关联的对象
@register.simple_tag
def display_all_realted_obj(obj):
    # ele = ''
    # ele += "<ul>"
    # for i in dir(obj):
    #     if str(i).endswith("_set"):
    #         parent = str(i)[:len(str(i))-4]
    #         ele += "<li>%s</li><ul>"% parent
    #         for obj in getattr(obj, str(i)).all():
    #             ele += "<li>%s</li>"% obj
    #         ele += "</ul>"
    # ele += "</ul>"

    ele = "<ul>"
    # ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a></li>" %(obj._meta.app_label,
    #                                                                  obj._meta.model_name,
    #                                                                  obj.id,obj)

    for reversed_fk_obj in obj._meta.related_objects:

        related_table_name = reversed_fk_obj.name
        related_lookup_key = "%s_set" % related_table_name
        related_objs = getattr(obj, related_lookup_key).all()  # 反向查所有关联的数据
        ele += "<li>%s3333<ul> " % related_table_name

        if reversed_fk_obj.get_internal_type() == "ManyToManyField":  # 不需要深入查找
            for i in related_objs:
                ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a> 记录里与[%s]相关的的数据将被删除</li>" \
                       % (i._meta.app_label, i._meta.model_name, i.id, i, obj)
        else:
            for i in related_objs:
                # ele += "<li>%s--</li>" %i
                ele += "<li><a href='/kingadmin/%s/%s/%s/change/'>%s</a></li>" % (i._meta.app_label,
                                                                                  i._meta.model_name,
                                                                                  i.id, i)
                ele += display_all_realted_obj(i)

        ele += "</ul></li>"

    ele += "</ul>"


    return ele

@register.simple_tag
def get_path(path):
    print('path------------->', path)
    return ''


