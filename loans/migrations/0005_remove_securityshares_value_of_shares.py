# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0004_auto_20151001_1748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='securityshares',
            name='value_of_shares',
        ),
    ]
