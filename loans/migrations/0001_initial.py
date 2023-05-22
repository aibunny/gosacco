# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0001_initial'),
        ('shares', '0001_initial'),
        ('members', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approval_date', models.DateTimeField()),
                ('amount', models.BigIntegerField(help_text=b'Actual amount approved')),
                ('payment_period', models.IntegerField(help_text=b'In days')),
                ('security_details', models.TextField(help_text=b'Basic info provided about the security')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('application_number', models.CharField(max_length=100)),
                ('application_date', models.DateField(auto_now_add=True)),
                ('amount', models.BigIntegerField()),
                ('purpose', models.CharField(help_text=b'Purpose for the loan', max_length=250)),
                ('payment_period', models.IntegerField(help_text=b'In Days')),
                ('status', models.CharField(default=b'pending', help_text=b'Current status of the application', max_length=25, choices=[(b'pending', b'Pending'), (b'approved', b'Approved'), (b'rejected', b'Rejected')])),
                ('security_details', models.TextField(help_text=b'Basic info provided about the security')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LoanRuleOther',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rule', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LoanRuleSavings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minimum', models.BigIntegerField()),
                ('maximum', models.BigIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LoanRuleShares',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minimum', models.BigIntegerField()),
                ('maximum', models.BigIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LoanType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('interest', models.FloatField()),
                ('interest_period', models.CharField(default=b'year', max_length=50, choices=[(b'year', b'per anum'), (b'month', b'per month'), (b'day', b'per day')])),
                ('processing_period', models.IntegerField(help_text=b'In days')),
                ('minimum_amount', models.BigIntegerField()),
                ('maximum_amount', models.BigIntegerField()),
                ('minimum_membership_period', models.IntegerField(help_text=b'In months(A month is 30 days)')),
                ('minimum_shares', models.BigIntegerField()),
                ('minimum_savings', models.BigIntegerField()),
                ('minimum_payback_period', models.IntegerField(help_text=b'In days')),
                ('maximum_payback_period', models.IntegerField(help_text=b'In days')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SecurityArticle',
            fields=[
                ('security_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loans.Security')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(help_text=b'eg Land, car, house', max_length=100)),
                ('identification_type', models.CharField(help_text=b'eg Land title, car logbook', max_length=100)),
                ('identification', models.CharField(help_text=b'eg ID Number, Title number', max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('loans.security',),
        ),
        migrations.CreateModel(
            name='SecuritySavings',
            fields=[
                ('security_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loans.Security')),
                ('savings_amount', models.BigIntegerField()),
                ('savings_type', models.ForeignKey(to='savings.SavingsType')),
            ],
            options={
                'abstract': False,
            },
            bases=('loans.security',),
        ),
        migrations.CreateModel(
            name='SecurityShares',
            fields=[
                ('security_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loans.Security')),
                ('number_of_shares', models.IntegerField()),
                ('value_of_shares', models.BigIntegerField(blank=True)),
                ('share_type', models.ForeignKey(to='shares.ShareType')),
            ],
            options={
                'verbose_name_plural': 'Security shares',
            },
            bases=('loans.security',),
        ),
        migrations.AddField(
            model_name='security',
            name='loan',
            field=models.ForeignKey(blank=True, to='loans.Loan', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='security',
            name='loan_application',
            field=models.ForeignKey(to='loans.LoanApplication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='security',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_loans.security_set+', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loanruleshares',
            name='loan_type',
            field=models.ForeignKey(related_name='shares_rules', to='loans.LoanType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loanruleshares',
            name='shares_type',
            field=models.ForeignKey(blank=True, to='shares.ShareType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loanrulesavings',
            name='loan_type',
            field=models.ForeignKey(related_name='savings_rules', to='loans.LoanType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loanrulesavings',
            name='savings_type',
            field=models.ForeignKey(blank=True, to='savings.SavingsType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loanruleother',
            name='loan_type',
            field=models.ForeignKey(related_name='extra_rules', to='loans.LoanType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='loan_type',
            field=models.ForeignKey(related_name='LoanType', to='loans.LoanType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='member',
            field=models.ForeignKey(to='members.Member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loan',
            name='application',
            field=models.ForeignKey(to='loans.LoanApplication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loan',
            name='loan_type',
            field=models.ForeignKey(to='loans.LoanType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loan',
            name='member',
            field=models.ForeignKey(to='members.Member'),
            preserve_default=True,
        ),
    ]
