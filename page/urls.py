# -*- coding: utf-8 -*-

from django.urls import path, re_path

from . import views

app_name = "page"

urlpatterns = [
    path(r'download/<int:file_id>', views.download, name='download'),
    path(r'download/<int:file_id>/<str:file_name>', views.download, name='download'),

    path('post/<int:post_id>/', views.post, name='post'),
    path('post/<str:cate_id>/', views.post_list, name='post_list'),

    path('<int:page_id>/', views.page, name='page_by_id'),
    path('<slug:page_code>/', views.page, name='page_by_code'),

    path('', views.home, name='home'),
]
