# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=50)),
                ('registration_date', models.DateField()),
                ('monthly_income', models.BigIntegerField()),
                ('occupation', models.CharField(max_length=50)),
                ('bank', models.CharField(max_length=100)),
                ('account_number', models.CharField(max_length=50)),
                ('signature', models.ImageField(upload_to=b'')),
                ('id_type', models.CharField(max_length=50)),
                ('id_number', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('nationality', models.CharField(max_length=50)),
                ('comments', models.TextField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NextOfKin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('relationship', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('occupation', models.CharField(max_length=50)),
                ('comments', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=100)),
                ('current_village', models.CharField(max_length=100)),
                ('current_subcounty', models.CharField(max_length=100)),
                ('current_district', models.CharField(max_length=100)),
                ('permanent_village', models.CharField(max_length=100)),
                ('permanent_subcounty', models.CharField(max_length=100)),
                ('permanent_district', models.CharField(max_length=100)),
                ('signature', models.ImageField(upload_to=b'')),
                ('member', models.OneToOneField(to='members.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='group',
            name='leader',
            field=models.ForeignKey(related_name='Group Leader', to='members.Member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='members.Member'),
            preserve_default=True,
        ),
    ]
