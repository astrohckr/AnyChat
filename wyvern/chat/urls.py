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
        name='detail'
    ),
    url(
        regex=r'^\w+/create',
        view=views.CreateGroup.as_view(),
        name='detail'
    ),
    url(
        regex=r'^\w+/(?P<name>\w+)$',
        view=views.GroupDetail.as_view(),
        name='detail'
    ),
]
