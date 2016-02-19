# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from anychat.anychat.views import login, categories, groups

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
        regex=r'^chat/(?P<category>\w+)/$',
        view=categories.CategoryDetail.as_view(),
        name='category_detail'
    ),

    url(
        regex=r'^chat/(?P<category>\w+)/create-group$',
        view=groups.GroupCreate.as_view(),
        name='group_create'
    ),

    url(
        regex=r'^chat/(?P<category>\w+)/group/(?P<group>\w+)$',
        view=groups.GroupChat.as_view(),
        name='group_chat'
    ),

    # url(r'^groups/', include("anychat.anychat.views.groups", namespace="groups")),
    # url(r'^categories/', include("anychat.anychat.views.categories", namespace="categories")),
]
