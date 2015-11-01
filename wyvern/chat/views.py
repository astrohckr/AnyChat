# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView
from wyvern.chat import models
from wyvern.chat.models import Group, Category


class CategoryList(ListView):
    model = Category


class CategoryDetail(DetailView):
    model = Category


class GroupDetail(DetailView):
    model = Group


class GroupCreate(CreateView):
    model = Group
    fields = ['name', 'description']

    # def __init__(self, *args, **kwargs):
    #     super(GroupCreate, self).__init__(*args, **kwargs)
    #
    #     self.fields['category'].queryset = Category.objects.filter(name=kwargs['category_name'])
    #     self.fields['url'].queryset = models.next_url()
