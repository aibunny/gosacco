from itertools import chain
from operator import attrgetter
from django.db import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models, Error


# Create your models here.
from django.db.models import ForeignKey, IntegerField, CharField, BigIntegerField, Q, DateTimeField, Sum, TextField
from django.utils import timezone
from members.models import Member, Group


class ShareType(models.Model):
    share_class = CharField(max_length=50)
    share_price = BigIntegerField()
    minimum_shares = BigIntegerField()
    maximum_shares = BigIntegerField()

    def __unicode__(self):
        return self.share_class

    @classmethod
    def get_share_types(cls):
        share_types = cls.object.objects.all()
        return share_types


class Shares(models.Model):
    member = ForeignKey(Member,on_delete=models.CASCADE)
    share_type = ForeignKey(ShareType,on_delete=models.CASCADE)
    number_of_shares = IntegerField()
    date = DateTimeField()

    class Meta:
        unique_together = ("member", "share_type")
        verbose_name_plural = 'Shares'

    def __unicode__(self):
        return ' '.join([self.member.user.first_name, self.member.user.last_name])

    def member_name(self):
        return ' '.join([self.member.user.first_name, self.member.user.last_name])

    @classmethod
    def get_shares(cls, members=None, current_share_type=None):
        """
        Get a shares for all or some members
        """
        if current_share_type is None:
            if members is None:
                shares = cls.objects.all()
            elif isinstance(members, Member):
                shares = cls.objects.filter(member=members)
            elif isinstance(members, Group):
                # TODO Refactor these two statements inot one query
                group_members = Member.objects.filter(group__pk=members.pk)
                shares = cls.objects.filter(member__in=group_members)
            elif isinstance(members, list):
                shares = cls.objects.filter(member__in=members)
        elif isinstance(current_share_type, ShareType):
            if members is None:
                shares = cls.objects.filter(share_type=current_share_type)
            elif isinstance(members, Member):
                shares = cls.objects.filter(member=members, share_type=current_share_type)
            elif isinstance(members, Group):
                # TODO Refactor these two statements inot one query
                group_members = Member.objects.filter(group__pk=members.pk)
                shares = cls.objects.filter(member__in=group_members, share_type=current_share_type)
            elif isinstance(members, list):
                shares = cls.objects.filter(member__in=members, share_type=current_share_type)
        else:
            shares = []

        return shares

    @classmethod
    def get_members_shares(cls, member, current_share_type=None):
        """
        Get a members shares
        """
        if current_share_type is None:
            shares = Shares.objects.filter(member=member)
        else:
            shares = Shares.objects.filter(share_type=current_share_type, member=member)
        return shares

    @classmethod
    def get_members_shares_total(cls, member):
        shares = cls.objects.filter(member=member).aggregate(Sum('number_of_shares'))
        return shares['number_of_shares__sum']

    @classmethod
    def get_share_transactions(cls, member):
        return sorted(
            chain(SharePurchase.get_share_purchases(member), ShareTransfer.get_share_transfers(member)),
            key=attrgetter('date'))


class SharePurchase(models.Model):
    member = ForeignKey(Member,on_delete=models.CASCADE)
    current_share_price = IntegerField(blank=True, )
    number_of_shares = IntegerField()
    date = DateTimeField(blank=True, auto_now_add=True)
    share_type = ForeignKey(ShareType,on_delete=models.CASCADE)

    def __unicode__(self):
        return str(
            self.number_of_shares) + " " + "class " + self.share_type.share_class + " shares bought by " + self.member.user.username  # +" at "+self.date

    @classmethod
    def issue_shares(cls, member, shares, share_type):
        """
        Issue new stock to member
        """
        try:
            share_price = share_type.share_price
            transfer = cls(member=member, number_of_shares=shares, current_share_price=share_price,
                           share_type=share_type, date=timezone.now())
            transfer.save()
            try:
                member_shares = Shares.objects.get(member=member, share_type=share_type)
                member_shares.number_of_shares += shares
                member_shares.save()
            except ObjectDoesNotExist:
                member_shares = Shares(member=member, number_of_shares=shares, share_type=share_type,
                                       date=timezone.now())
                member_shares.save()
        except Error as e:
            # print e
            return False

        return True

    @classmethod
    def get_share_purchases(cls, members=None, current_share_type=None):
        """
        Get a shares for all or some members
        """
        if current_share_type is None:
            if members is None:
                shares_purchases = cls.objects.all()
            elif isinstance(members, Member):
                shares_purchases = cls.objects.filter(member=members)
            elif isinstance(members, Group):
                # TODO Refactor these two statements inot one query
                group_members = Member.objects.filter(group__pk=members.pk)
                shares_purchases = cls.objects.filter(member__in=group_members)
            elif isinstance(members, list):
                shares_purchases = cls.objects.filter(member__in=members)
        elif isinstance(current_share_type, ShareType):
            if members is None:
                shares_purchases = cls.objects.filter(share_type=current_share_type)
            elif isinstance(members, Member):
                shares_purchases = cls.objects.filter(member=members, share_type=current_share_type)
            elif isinstance(members, Group):
                # TODO Refactor these two statements inot one query
                group_members = Member.objects.filter(group__pk=members.pk)
                shares_purchases = cls.objects.filter(member__in=group_members, share_type=current_share_type)
            elif isinstance(members, list):
                shares_purchases = cls.objects.filter(member__in=members, share_type=current_share_type)
        else:
            shares_purchases = []

        return shares_purchases


class ShareTransfer(models.Model):
    seller = ForeignKey(Member, related_name="Sender",on_delete=models.CASCADE)
    buyer = ForeignKey(Member, related_name="Recepient",on_delete=models.CASCADE)
    reason = TextField(null=True, blank=True)
    share_type = ForeignKey(ShareType,on_delete=models.CASCADE)
    number_of_shares = IntegerField()
    current_share_price = IntegerField()
    date = DateTimeField()

    def __unicode__(self):
        return str(
            self.number_of_shares) + " " + "class " + self.share_type.share_class + " shares from " + self.seller.user.username + " to " + self.buyer.user.username

    @classmethod
    def transfer_shares(cls, seller, buyer, number_of_shares, share_type, reason=None):
        """
        Transfer shares from one member to another

        """
        try:
            seller_shares = Shares.objects.get(member=seller, share_type=share_type)
        except Shares.DoesNotExist:
            return ValidationError(
                {"share_type": "You do not posses any shares of type" + share_type.__str__()})

        try:
            buyer_shares = Shares.objects.get(member=buyer, share_type=share_type)
        except ObjectDoesNotExist:
            buyer_shares = Shares(member=buyer, share_type=share_type, number_of_shares=0, date=timezone.now())
            buyer_shares.save()

        if seller_shares.number_of_shares < number_of_shares:
            return ValidationError(
                {"number_of_shares": "You do not have enough shares of type " + share_type.__str__()})

        else:
            transfer = ShareTransfer(seller=seller, buyer=buyer, number_of_shares=number_of_shares,
                                     share_type=share_type, date=timezone.now(),
                                     current_share_price=share_type.share_price, reason=reason)

            buyer_shares.number_of_shares += number_of_shares
            seller_shares.number_of_shares -= number_of_shares

            transfer.save()
            buyer_shares.save()
            seller_shares.save()
        return transfer

    @classmethod
    def get_share_transfers(cls, members=None, seller=None, buyer=None, current_share_type=None):
        """
        Get a shares for all or some members
        """
        if current_share_type is None:
            if members is None and seller is None and buyer is None:
                shares_transfer = cls.objects.all()
            elif members is not None and isinstance(members, Member):
                """
                Get all transfers where a Member is involved as buyer or seller
                """
                shares_transfer = cls.objects.filter(Q(buyer=members) | Q(seller=members))

            elif isinstance(seller, Member) and buyer is not None:
                shares_transfer = cls.objects.filter(seller=seller)

            elif isinstance(buyer, Member) and seller is None:
                shares_transfer = cls.objects.filter(buyer=buyer)

            elif isinstance(buyer, Member) and isinstance(seller, Member):
                shares_transfer = cls.objects.filter(buyer=buyer, seller=seller)

            elif isinstance(members, Group):
                # TODO Refactor these two statements inot one query
                group_members = Member.objects.filter(group__pk=members.pk)
                shares_transfer = cls.objects.filter(Q(seller__in=group_members) | Q(buyer__in=group_members))

            elif isinstance(members, list):
                shares_transfer = cls.objects.filter(Q(seller__in=members) | Q(buyer__in=members))

        elif isinstance(current_share_type, ShareType):
            if members is None and seller is None and buyer is None:
                shares_transfer = cls.objects.filter(share_type=current_share_type)
            elif members is not None and isinstance(members, Member):
                """
                Get all transfers where a Member is involved as buyer or seller
                """
                shares_transfer = cls.objects.filter(Q(buyer=members) | Q(seller=members),
                                                     share_type=current_share_type)

            elif isinstance(seller, Member) and buyer is not None:
                shares_transfer = cls.objects.filter(seller=seller, share_type=current_share_type, )

            elif isinstance(buyer, Member) and seller is None:
                shares_transfer = cls.objects.filter(buyer=buyer, share_type=current_share_type, )

            elif isinstance(buyer, Member) and isinstance(seller, Member):
                shares_transfer = cls.objects.filter(buyer=buyer, seller=seller, share_type=current_share_type, )

            elif isinstance(members, Group):
                # TODO Refactor these two statements inot one query
                group_members = Member.objects.filter(group__pk=members.pk)
                shares_transfer = cls.objects.filter(Q(seller__in=group_members) | Q(buyer__in=group_members),
                                                     share_type=current_share_type, )

            elif isinstance(members, list):
                shares_transfer = cls.objects.filter(Q(seller__in=members) | Q(buyer__in=members),
                                                     share_type=current_share_type)
        else:
            shares_transfer = []

        return shares_transfer
