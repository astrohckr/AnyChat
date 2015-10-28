# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from wyvern.chat.models import Group, Category


class CategoryList(ListView):
    model = Category


class CategoryDetail(DetailView):
    model = Category


class GroupDetail(DetailView):
    model = Group


class CreateGroup(DetailView):
    model = Group


class CategoryForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=255)
