# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityGuarantor',
            fields=[
                ('security_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loans.Security')),
                ('number_of_shares', models.IntegerField()),
                ('share_type', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('member', models.ForeignKey(to='members.Member')),
            ],
            options={
                'abstract': False,
            },
            bases=('loans.security',),
        ),
    ]
