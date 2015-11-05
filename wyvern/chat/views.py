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
    success_url = '/%(category)s/%(slug)s'

    def form_valid(self, form):
        form.instance.category = get_object_or_404(Category, name=self.kwargs.get('category'))
        form.instance.url = models.next_slug()
        form.instance.point = 'POINT(0.0 0.0)'
        return super(GroupCreate, self).form_valid(form)

        # def get_success_url(self):
        #     category = self.object.category.name
        #     group = self.object.slug
        #     return '/%s/%s' % ("s", "")
