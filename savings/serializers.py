from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from members.serializers import MemberSerializer, MemberUserSerializer

from savings.models import Savings, SavingsType, SavingsDeposit, SavingsWithdrawal
from django.contrib.auth.models import User
from members.models import Member, Group, NextOfKin



class SavingsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsType
        fields = ('id','name','category','compulsory','interval','minimum_amount','maximum_amount','interest')


class SavingsSerializer(serializers.ModelSerializer):
    member = MemberSerializer()
    savings_type = SavingsTypeSerializer()

    class Meta:
        model = Savings
        fields = ('id','member','amount','date','savings_type')

class CreateSavingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Savings
        fields = ('id','member','amount','date','savings_type')


class SavingsWithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsWithdrawal
        fields = ('id','amount','date','member','savings_type')




class SavingsMinimalSerializer(serializers.ModelSerializer):
    member = MemberUserSerializer()
    savings_type = SavingsTypeSerializer()

    class Meta:
        model = Savings
        fields = ('id','member','amount','date','savings_type')


class SavingsDepositMinimalSerializer(serializers.ModelSerializer):
    member = MemberUserSerializer()

    class Meta:
        model = SavingsDeposit
        fields = ('id','member','amount','date','savings_type')


class SavingsDepositPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsDeposit
        fields = ('amount', 'savings_type')


class SavingsWithdrawalMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavingsWithdrawal
        fields = ('id','member','amount','date','savings_type')


class SavingsWithdrawalPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavingsWithdrawal
        fields = ('amount', 'savings_type')


class SavingsWithdrawalTransactionSerializer(serializers.ModelSerializer):
    member = MemberUserSerializer()
    transaction_type = serializers.SerializerMethodField()

    class Meta:
        model = SavingsWithdrawal

    def get_transaction_type(self,obj):
        return obj.__class__.__name__


class SavingsDepositTransactionSerializer(serializers.ModelSerializer):
    member = MemberUserSerializer()
    transaction_type = serializers.SerializerMethodField()

    class Meta:
        model = SavingsDeposit

    def get_transaction_type(self,obj):
        return obj.__class__.__name__

class SavingsTransactionsMinimalSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        """
        Transactions can be deposits or withdrawals
        """
        if isinstance(obj, SavingsDeposit):
            return SavingsDepositTransactionSerializer(obj, context=self.context). to_representation(obj)
        elif isinstance(obj, SavingsWithdrawal):
            return SavingsWithdrawalTransactionSerializer(obj, context=self.context). to_representation(obj)
        return super(SavingsDepositTransactionSerializer, self). to_representation(obj)
