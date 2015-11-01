# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from Tools.scripts.texi2html import increment
from math import floor

from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):
    id = models.AutoField(primary_key=True, default=0)
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, default='Description')

    def __str__(self):
        return self.name


def next_url():
    a_0 = Group.objects.count()
    rs = []  # remainders
    url = ""

    # apply the division algorithm
    while a_0 > 0:
        a = floor(a_0 / 52)
        r = a_0 - a * 52
        rs.append(r)

    for r in reversed(rs):
        if r < 32:
            char = r + 97
        else:
            char = r + 33
        url += chr(char)  # add ascii character to url

    return url


@python_2_unicode_compatible
class Group(models.Model):
    category = models.ForeignKey(Category)
    url = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255, default='Description')
    closed = models.BooleanField(default=False)
    point = models.PointField(default='POINT(0.0 0.0)')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/chat/%s/%s' % (self.category.name, self.id)
