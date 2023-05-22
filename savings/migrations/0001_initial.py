# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Savings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(to='members.Member')),
            ],
            options={
                'verbose_name_plural': 'Savings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SavingsDeposit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('member', models.ForeignKey(to='members.Member')),
            ],
            options={
                'verbose_name_plural': 'Savings Purchase',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SavingsType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(default=b'fixed', max_length=50, choices=[(b'fixed', b'fixed'), (b'contract', b'contract'), (b'current', b'current'), (b'target', b'target')])),
                ('compulsory', models.BooleanField(default=True)),
                ('interval', models.CharField(default=b'month', max_length=50, choices=[(b'year', b'per anum'), (b'month', b'per month'), (b'week', b'per week'), (b'day', b'per day')])),
                ('minimum_amount', models.IntegerField()),
                ('maximum_amount', models.IntegerField()),
                ('interest', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SavingsWithdrawal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('member', models.ForeignKey(to='members.Member')),
                ('savings_type', models.ForeignKey(to='savings.SavingsType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='savingsdeposit',
            name='savings_type',
            field=models.ForeignKey(to='savings.SavingsType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='savings',
            name='savings_type',
            field=models.ForeignKey(to='savings.SavingsType'),
            preserve_default=True,
        ),
    ]
