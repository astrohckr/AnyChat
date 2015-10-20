# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.contrib.gis.geos.point import Point
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Group(models.Model):
    category = models.ForeignKey(Category)
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255, default='Description')
    point = models.PointField(default='POINT(0.0 0.0)')

    def __str__(self):
        return self.name
