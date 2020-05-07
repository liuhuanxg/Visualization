#-*-coding:utf-8 -*-
"""
@File: add_data.py
@作用：这个文件用来模拟数据
"""

from .models import LongitudeLatitude, Geographic_Information, Geology
from django.http import HttpResponse
import random

# 添加经纬度信息
def add_LongitudeLatitude(request):
    for j in range(2):
        if j==0:
            for i in range(180):
                for z in range(1,10):
                    LongitudeLatitude.objects.create(
                        longitude="东经{}".format(i),
                        latitude="南纬{}".format(z)
                    )
                    LongitudeLatitude.objects.create(
                        longitude="东经{}".format(i),
                        latitude="北纬{}".format(z)
                    )
        if j == 1:
            for i in range(180):
                for z in range(1, 10):
                    LongitudeLatitude.objects.create(
                        longitude="西经{}".format(i),
                        latitude="南纬{}".format(z)
                    )
                    LongitudeLatitude.objects.create(
                        longitude="西经{}".format(i),
                        latitude="北纬{}".format(z)
                    )
    return HttpResponse("经纬度添加成功")


# 添加地质
def add_geology(request):
    geology_lst = {"土壤":10001, "岩石":10002, "煤炭":10003, "矿物质":10004, "石油":10005}
    for key, value in geology_lst.items():
        Geology.objects.create(
            geology_name = key,
            number = value
        )
    return HttpResponse("地质添加成功！")

# 添加地理数据信息
def add_geo_information(request):
    l_lst = LongitudeLatitude.objects.values_list("id", flat=True)
    g_lst = Geology.objects.values_list("id", flat=True)
    for i in l_lst:
        for g in g_lst:
            Geographic_Information.objects.create(
                geology_id=g,
                longitudelatitude_id=i,
                depth=random.randint(10,1000),
            )
    return HttpResponse("地理数据添加成功！")





