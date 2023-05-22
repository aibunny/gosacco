# Create your views here.
from django.core.exceptions import ValidationError

from django.http.response import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from members.models import Member
from members.permissions import IsOwnerOrAdmin
from savings.models import Savings, SavingsType, SavingsWithdrawal, SavingsDeposit
from savings.serializers import SavingsMinimalSerializer, SavingsDepositMinimalSerializer, \
    SavingsWithdrawalMinimalSerializer, \
    SavingsTransactionsMinimalSerializer, SavingsDepositPostSerializer, SavingsWithdrawalPostSerializer


class SavingsView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_member(self, pk):
        """
        Get a member.
        """
        try:
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        List Member's savings
        ---
        serializer: savings.serializers.SavingsMinimalSerializer
        """
        if pk is not None:
            member = self.get_member(int(pk))
        else:
            member = None
        self.check_object_permissions(request, member)
        savings = Savings.get_members_savings(member)
        serializer = SavingsMinimalSerializer(savings, many=True)
        return Response(serializer.data)


class SavingsDepositView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_member(self, pk):
        """
        Get a member.
        """
        try:
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        List Member's savings Deposits
        ---
        serializer: savings.serializers.SavingsDepositMinimalSerializer
        """
        if pk is not None:
            member = self.get_member(int(pk))
        else:
            member = None
        self.check_object_permissions(request, member)
        deposits = SavingsDeposit.get_savings_deposits(member)
        serializer = SavingsDepositMinimalSerializer(deposits, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        """
        Deposit Memeber's Savings
        ---
        serializer: savings.serializers.SavingsDepositPostSerializer
        """
        member = self.get_member(pk)
        self.check_object_permissions(request, member)
        serializer = SavingsDepositPostSerializer(data=request.data)
        if serializer.is_valid():
            savings_added = SavingsDeposit.deposit_savings(member=member,
                                                           savings_type=serializer.validated_data['savings_type'],
                                                           amount=serializer.validated_data['amount'])
            if savings_added:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavingsWithdrawalView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_member(self, pk):
        """
        Get a member.
        """
        try:
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        List Member's savings Deposits
        ---
        serializer: savings.serializers.SavingsWithdrawalMinimalSerializer
        """
        if pk is not None:
            member = self.get_member(int(pk))
        else:
            member = None
        self.check_object_permissions(request, member)
        deposits = SavingsWithdrawal.get_withdrawals(member)
        serializer = SavingsWithdrawalMinimalSerializer(deposits, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        """
        Deposit Memeber's Savings
        ---
        serializer: savings.serializers.SavingsWithdrawalPostSerializer
        """
        member = self.get_member(pk)
        self.check_object_permissions(request, member)
        serializer = SavingsWithdrawalPostSerializer(data=request.data)
        if serializer.is_valid():
            savings_withdrawn = SavingsWithdrawal.withdraw_savings(member=member,
                                                                   savings_type=serializer.validated_data['savings_type'],
                                                                   amount=serializer.validated_data['amount'])
            if isinstance(savings_withdrawn, ValidationError):
                return Response(savings_withdrawn, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SavingsTransactionsView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_member(self, pk):
        """
        Get a member.
        """
        try:
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        List Member's savings Deposits
        """
        if pk is not None:
            member = self.get_member(int(pk))
        else:
            member = None
        self.check_object_permissions(request, member)
        transactions = Savings.get_savings_transactions(member)
        serializer = SavingsTransactionsMinimalSerializer(transactions, many=True)
        return Response(serializer.data)
