# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0003_auto_20150930_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='comment',
            field=models.TextField(help_text=b'Feedback from management', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='security',
            name='value',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
