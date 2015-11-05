# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from wyvern.chat import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.CategoryList.as_view(),
        name='list'
    ),
    url(
        regex=r'^(?P<name>\w+)/$',
        view=views.CategoryDetail.as_view(),
        name='categoryDetail'
    ),
    url(
        regex=r'^(?P<category>\w+)/create-group$',
        view=views.GroupCreate.as_view(),
        name='groupCreate'
    ),
    url(
        regex=r'^\w+/(?P<slug>\w+)$',
        view=views.GroupDetail.as_view(),
        name='groupDetail'
    ),
]
