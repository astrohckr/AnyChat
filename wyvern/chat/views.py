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

    def get_initial(self):
        category = get_object_or_404(Category, name=self.kwargs.get('category'))
        url = models.next_url()
        point = 'POINT(0.0 0.0)'
        return {
            'category': category,
            'url': url,
            'point': point,
        }
