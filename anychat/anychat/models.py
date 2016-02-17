# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from math import floor

from django.contrib.gis.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True, default=0)
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, default='Description')

    def __str__(self):
        return self.name


class Group(models.Model):
    category = models.ForeignKey(Category)
    slug = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255, default='Description')
    closed = models.BooleanField(default=False)
    point = models.OneToOneField('Point')
    # setting = models.OneToOneField(UserSetting)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/chat/%s/%s' % (self.category.name, self.id)


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

    def __str__(self):
        return self.name


def next_slug():
    """
    Creates a slug for a new group.
    The slug is created from the number of existing groups.

    This is just changing the base and using letters of both cases.
    """

    a_0 = Group.objects.count() + 1
    rs = []  # remainders
    url = ""

    # apply the division algorithm
    while a_0 > 0:
        a = floor(a_0 / 52)
        r = a_0 - a * 52
        a_0 = a
        rs.append(r)

    for r in reversed(rs):
        if r < 32:
            char = r + 97
        else:
            char = r + 33
        url += chr(char)  # add ascii character to url

    return url
