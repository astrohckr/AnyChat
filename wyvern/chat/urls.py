# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from wyvern.chat import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.GroupList.as_view(),
        name='list'
    ),
    url(
        regex=r'^/add/$',
        view=views.GroupList.as_view(),
        name='list'
    ),
]
