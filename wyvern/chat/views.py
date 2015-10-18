# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.views.generic.list import ListView
from wyvern.chat.models import Group


class GroupList(ListView):
    model = Group


class CategoryList(ListView):
    model = Group
