# _*_ coding: utf-8 _*_
# @time     : 2018/5/16 14:10
# @Author   : liying
# @FileName : urls.py
# @Software : PyCharm

from django.urls import path

from Film_App import views

urlpatterns = [
    path('', views.index),
    path('getInfo/', views.getInfo),
    path('getList/', views.getList),
    path('search/', views.search),
    path('login/', views.login),
    path('register/', views.register),
    path('getInfo_nlogin/', views.getInfo_nlogin),
    path('verify/', views.verify),
    path('collect/', views.collect),
    path('cancel_collect/', views.cancel_collect),
    path('getMyCollection/', views.getMyCollection),
    path('qrcode/', views.generate_qrcode),
    path('zan/', views.zan),
    path('cai/', views.cai),
    path('comment/', views.comment),
    path('write_comment/', views.write_comment),
    path('send_barrage/', views.send_barrage),
    path('get_barrage/', views.get_barrage),
]