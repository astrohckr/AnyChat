# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from math import floor
from autoslug.fields import AutoSlugField

from django.contrib.gis.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, default='Description')

    slug = AutoSlugField(populate_from='name')

    def __str__(self):
        return self.name


class Group(models.Model):
    category = models.ForeignKey(Category)

    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255, default='Description')

    closed = models.BooleanField(default=False)
    point = models.OneToOneField('Point')
    # setting = models.OneToOneField(UserSetting)

    slug = AutoSlugField(populate_from='name', unique_with='category')

    def __str__(self):
        return self.name


# class GroupSetting(models.Model):

class User(models.Model):
    group = models.ForeignKey(Group, null=True, blank=True)
    uuid = models.UUIDField(unique=True)
    point = models.OneToOneField('Point')

    # setting = models.OneToOneField(UserSetting)


# class UserSetting(models.Model):


class Point(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
