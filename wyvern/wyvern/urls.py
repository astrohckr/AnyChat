# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from wyvern.wyvern.views import login, categories, groups

urlpatterns = [
    url(
        regex=r'^login/$',
        view=login.login,
        name='login'
    ),

    url(
        regex=r'^chat/$',
        view=categories.CategoryList.as_view(),
        name='list'
    ),

    url(
        regex=r'^chat/(?P<name>\w+)/$',
        view=categories.CategoryDetail.as_view(),
        name='categoryDetail'
    ),

    url(
        regex=r'^chat/(?P<category>\w+)/create-group$',
        view=groups.GroupCreate.as_view(),
        name='groupCreate'
    ),

    url(
        regex=r'^chat/(?P<category>\w+)/group/(?P<slug>\w+)$',
        view=groups.GroupDetail.as_view(),
        name='groupDetail'
    ),

    # url(r'^groups/', include("wyvern.wyvern.views.groups", namespace="groups")),
    # url(r'^categories/', include("wyvern.wyvern.views.categories", namespace="categories")),
]
