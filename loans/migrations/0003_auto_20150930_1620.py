# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0002_securityguarantor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='securityguarantor',
            old_name='member',
            new_name='guarantor',
        ),
        migrations.AlterField(
            model_name='securityguarantor',
            name='share_type',
            field=models.ForeignKey(to='shares.ShareType'),
            preserve_default=True,
        ),
    ]
