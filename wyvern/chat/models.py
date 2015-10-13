# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=30)


@python_2_unicode_compatible
class Group(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=30)
