#-*-coding:utf-8 -*-
"""
@File: urls.py
"""

from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('index/', index, name="index"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('search/', search, name="search"),

    # 经纬度信息操作
    path('longitudelatitude_message/', longitudelatitude_message, name="longitudelatitude_message"),
    path('longitudelatitude_detail/<int:id>', longitudelatitude_detail, name="longitudelatitude_detail"),
    path('delete_longitudelatitude_message/<int:id>', delete_longitudelatitude_message, name="delete_longitudelatitude_message"),

    # ajax 数据接口
    path('data_detail/', data_detail, name="data_detail"),
    path('get_all_message/', get_all_message, name="get_all_message"),
    path('get_message/<str:keywords>', get_message, name="get_message"),

    # 地理信息操作
    path('geographic_information/', geographic_information, name="geographic_information"),
    path('add_geographic_information/', add_geographic_information, name="add_geographic_information"),
    path('delete_geographic_information/<int:id>', delete_geographic_information, name="delete_geographic_information"),
    path('update_geographic_information/<int:id>', update_geographic_information, name="update_geographic_information"),

   # 地质信息操作
    path('geology_message/', geology_message, name="geology_message"),
    path('delete_geology_message/<int:id>', delete_geology_message, name="delete_geology_message"),
    path('update_geology_message/<int:id>', update_geology_message, name="update_geology_message"),
    path('add_geology_message/', add_geology_message, name="add_geology_message"),

    # 遥感图像匹配
    path('image_matching/', image_matching, name="image_matching"),
]

app_name = "home"


# 模拟添加数据的测试接口，可不使用
from .add_data import *
urlpatterns +=[
    # path('add_LongitudeLatitude/', add_LongitudeLatitude, name="add_LongitudeLatitude"),
    # path('add_geology/', add_geology, name="add_geology"),
    # path('add_geo_information/', add_geo_information, name="add_geo_information"),
]