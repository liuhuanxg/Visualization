#-*-coding:utf-8 -*-
"""
@File: common.py
@作用：这个文件用来处理非视图逻辑
"""

from django.core.paginator import Paginator  #引入分页器
def set_page(data,num,page):
    """
    :param data: 所有的数据
    :param num:  每页的数据
    :param page: 当前的页码
    :return:
    """
    p = Paginator(data,num)
    number = p.num_pages
    page_range = p.page_range
    try:
        page = int(page)
        data = p.page(page)
    except:
        data = p.page(1)
    if page < 5:  # 一次只返回5个页码
        page_list = page_range[:5]
    elif page + 4 > number:
        page_list = page_range[-5:]
    else:
        page_list = page_range[page - 3:page + 2]
    return data,page_list


from django.http import HttpResponseRedirect
# 用户的登陆校验
def user_login_valid(func):
    def inner(request,*args,**kwargs):
        #通过key值是否在session和cookie中去校验
        if 'username' in request.session and 'username' in request.COOKIES:
            return func(request,*args,**kwargs)
        return HttpResponseRedirect('/login')
    return inner