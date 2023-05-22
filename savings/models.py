from itertools import chain
from operator import attrgetter

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models


# Create your models here.
from django.db.models import ForeignKey, IntegerField, CharField, BooleanField, DateTimeField, Sum
from django.utils import timezone
from members.models import Member, Group


class SavingsType(models.Model):
    YEAR = 'year'
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'
    INTERVAL_CHOICES = (
        (YEAR, 'per anum'),
        (MONTH, 'per month'),
        (WEEK, 'per week'),
        (DAY, 'per day'),
    )

    FIXED = 'fixed'
    CONTRACT = 'contract'
    CURRENT = 'current'
    TARGET = 'target'

    CATEGORY_CHOICES = (
        (FIXED, 'fixed'),
        (CONTRACT, 'contract'),
        (CURRENT, 'current'),
        (TARGET, 'target'),
    )
    name = CharField(max_length=100)
    category = CharField(max_length=50, choices=CATEGORY_CHOICES, default=FIXED)
    compulsory = BooleanField(default=True)
    interval = CharField(max_length=50, choices=INTERVAL_CHOICES, default=MONTH)
    minimum_amount = IntegerField()
    maximum_amount = IntegerField()
    interest = IntegerField()

    def __unicode__(self):
        return self.name

    def interest_rate(self):
        return str(self.interest) + "%"


class Savings(models.Model):
    class Meta:
        verbose_name_plural = 'Savings'

    member = ForeignKey(Member,on_delete=models.CASCADE)
    amount = IntegerField()
    date = DateTimeField(auto_now_add=True)
    savings_type = ForeignKey(SavingsType,on_delete=models.CASCADE)

    def __unicode__(self):
        return ' '.join([self.member.user.first_name, self.member.user.last_name])

    def member_name(self):
        return ' '.join([self.member.user.first_name, self.member.user.last_name])

    @classmethod
    def get_members_savings(cls, member, current_savings_type=None):
        if current_savings_type is None:
            savings = cls.objects.filter(member=member)
        else:
            savings = cls.objects.filter(savings_type=current_savings_type, member=member)
        return savings

    @classmethod
    def get_members_savings_total(cls, member):
        savings = cls.objects.filter(member=member).aggregate(Sum('amount'))
        return savings['amount__sum']

    @classmethod
    def get_savings(cls, members=None, current_savings_type=None):
        savings = []
        if current_savings_type is None:
            if members is None:
                savings = cls.objects.all()
            elif isinstance(members, Member):
                savings = cls.objects.filter(member=members)
            elif isinstance(members, Group):
                # TODO Refactor these two statements into one query
                group_members = Member.objects.filter(group__pk=members.pk)
                savings = cls.objects.filter(member__in=group_members)
            elif isinstance(members, list):
                savings = cls.objects.filter(member__in=members)
        elif isinstance(current_savings_type, SavingsType):
            if members is None:
                savings = cls.objects.filter(savings_type=current_savings_type)
            elif isinstance(members, Member):
                savings = cls.objects.filter(member=members, savings_type=current_savings_type)
            elif isinstance(members, Group):
                # TODO Refactor these two statements into one query
                group_members = Member.objects.filter(group__pk=members.pk)
                savings = cls.objects.filter(member__in=group_members, savings_type=current_savings_type)
            elif isinstance(members, list):
                savings = cls.objects.filter(member__in=members, savings_type=current_savings_type)

        return savings

    @classmethod
    def get_savings_transactions(self, member):
        return sorted(
            chain(SavingsDeposit.get_savings_deposits(member), SavingsWithdrawal.get_withdrawals(member)),
            key=attrgetter('date'))


class SavingsWithdrawal(models.Model):
    amount = IntegerField()
    date = DateTimeField()
    member = ForeignKey(Member,on_delete=models.CASCADE)
    savings_type = ForeignKey(SavingsType,on_delete=models.PROTECT)

    @classmethod
    def withdraw_savings(cls, member, savings_type, amount):

        try:
            savings = Savings.objects.get(member=member, savings_type=savings_type)
        except ObjectDoesNotExist:
            return ValidationError(
                {"savings_type": "You do not posses any savings of type" + savings_type.__str__()})
        if savings < amount:
            return ValidationError(
                {"amount": "You do not have enough savings of type" + savings_type.__str__()})

        savings_withdrawal = cls(amount=amount, member=member, savings_type=savings_type, date=timezone.now())
        savings.amount -= amount
        savings_withdrawal.save()
        savings.save()
        return savings_withdrawal

    @classmethod
    def get_withdrawals(cls, members=None, current_savings_type=None):
        if current_savings_type is None:
            if members is None:
                withdrawals = cls.objects.all()
            elif isinstance(members, Member):
                withdrawals = cls.objects.filter(member=members)
            elif isinstance(members, Group):
                # TODO Refactor these two statements inot one query
                group_members = Member.objects.filter(group__pk=members.pk)
                withdrawals = cls.objects.filter(member__in=group_members)
            elif isinstance(members, list):
                withdrawals = cls.objects.filter(member__in=members)
        elif isinstance(current_savings_type, SavingsType):
            if members is None:
                withdrawals = cls.objects.filter(savings_type=current_savings_type)
            elif isinstance(members, Member):
                withdrawals = cls.objects.filter(member=members, savings_type=current_savings_type)
            elif isinstance(members, Group):
                # TODO Refactor these two statements inot one query
                group_members = Member.objects.filter(group__pk=members.pk)
                withdrawals = cls.objects.filter(member__in=group_members, savings_type=current_savings_type)
            elif isinstance(members, list):
                withdrawals = cls.objects.filter(member__in=members, savings_type=current_savings_type)
        else:
            withdrawals = []
        return withdrawals


class SavingsDeposit(models.Model):
    amount = IntegerField()
    date = DateTimeField(blank=True, auto_now_add=True)
    member = ForeignKey(Member,on_delete=models.CASCADE)
    savings_type = ForeignKey(SavingsType,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Savings Purchase'

    @classmethod
    def deposit_savings(cls, member, savings_type, amount, date=timezone.now()):
        try:
            savings = Savings.objects.get(member=member, savings_type=savings_type)
            savings.amount += amount

        except ObjectDoesNotExist:
            savings = Savings(member=member, savings_type=savings_type, amount=amount, date=date)

        finally:
            deposit = cls(member=member, savings_type=savings_type, amount=amount, date=date)
            deposit.save()
            savings.save()
            return deposit

    @classmethod
    def get_savings_deposits(cls, members=None, current_savings_type=None):
        if current_savings_type is None:
            if members is None:
                savings_deposits = cls.objects.all()
            elif isinstance(members, Member):
                savings_deposits = cls.objects.filter(member=members)
            elif isinstance(members, Group):
                # TODO Refactor these two statements inot one query
                group_members = Member.objects.filter(group__pk=members.pk)
                savings_deposits = cls.objects.filter(member__in=group_members)
            elif isinstance(members, list):
                savings_deposits = cls.objects.filter(member__in=members)
        elif isinstance(current_savings_type, SavingsType):
            if members is None:
                savings_deposits = cls.objects.filter(savings_type=current_savings_type)
            elif isinstance(members, Member):
                savings_deposits = cls.objects.filter(member=members, savings_type=current_savings_type)
            elif isinstance(members, Group):
                # TODO Refactor these two statements inot one query
                group_members = Member.objects.filter(group__pk=members.pk)
                savings_deposits = cls.objects.filter(member__in=group_members, savings_type=current_savings_type)
            elif isinstance(members, list):
                savings_deposits = cls.objects.filter(member__in=members, savings_type=current_savings_type)
        else:
            savings_deposits = []

        return savings_deposits
