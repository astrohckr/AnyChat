# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20151012_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.CharField(max_length=255, default=''),
        ),
    ]
