from rest_framework import serializers

from members.serializers import MemberSerializer
from shares.models import ShareType, Shares, SharePurchase, ShareTransfer


class ShareTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareType
        fields = ('id', 'share_class', 'share_price', 'minimum_shares', 'maximum_shares')


class SharesSerializer(serializers.ModelSerializer):
    share_type = ShareTypeSerializer()
    member = MemberSerializer()

    class Meta:
        model = Shares
        fields = ('id', 'member', 'share_type', 'number_of_shares', 'date')


class SharesMinimalSerializer(serializers.ModelSerializer):
    share_type = ShareTypeSerializer()

    class Meta:
        model = Shares
        fields = ('id', 'share_type', 'number_of_shares', 'date')


class SharePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharePurchase


class SharePurchasePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharePurchase
        fields = ('share_type', 'number_of_shares')


class ShareTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareTransfer


class ShareTransferPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareTransfer
        fields = ('buyer', 'share_type', 'number_of_shares')


class SharePurchaseTransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.SerializerMethodField()

    class Meta:
        model = SharePurchase

    def get_transaction_type(self, obj):
        return obj.__class__.__name__


class ShareTransferTransactionSerializer(serializers.ModelSerializer):
    transaction_type = serializers.SerializerMethodField()

    class Meta:
        model = ShareTransfer

    def get_transaction_type(self, obj):
        return obj.__class__.__name__


class ShareTransactionsSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        """
        Transactions can be deposits or withdrawals
        """
        if isinstance(obj, SharePurchase):
            return SharePurchaseTransactionSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, ShareTransfer):
            return ShareTransferTransactionSerializer(obj, context=self.context).to_representation(obj)
        return super(SharePurchaseTransactionSerializer, self).to_representation(obj)
