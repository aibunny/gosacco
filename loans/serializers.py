from django.contrib.auth.models import User
from rest_framework import serializers, viewsets

from members.models import Member, Group, NextOfKin
from loans.models import LoanApplication, Security, SecurityShares, SecuritySavings, SecurityArticle, SecurityGuarantor, \
    Loan
from members.serializers import MemberSerializer, MemberUserSerializer


class LoanSerializer(serializers.ModelSerializer):
    member = MemberUserSerializer()

    class Meta:
        model = Loan


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication


class LoanApplicationWithSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication


class LoanApplicationPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanApplication
        fields = (
        'application_number', 'amount', 'purpose', 'payment_period', 'security_details', 'loan_type',)


class SecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Security

    def to_representation(self, obj):
        """
        The Serializer is selected depending on the type of security
        """
        if isinstance(obj, SecuritySavings):
            return SecuritySavingsSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, SecurityShares):
            return SecuritySharesSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, SecurityArticle):
            return SecurityArticleSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, SecurityGuarantor):
            return SecurityGuarantorSerializer(obj, context=self.context).to_representation(obj)

        return super(SecuritySerializer, self).to_representation(obj)

    def to_internal_value(self, data):
        """
        The Serializer is selected depending on the type of security
        """
        if data.get('security_type') == 'security savings':
            return SecuritySavingsSerializer(data)
        elif data.get('security_type') == 'security shares':
            return SecuritySharesSerializer(data)
        elif data.get('security_type') == 'security article':
            return SecurityArticleSerializer(data)
        elif data.get('security_type') == 'security guarantor':
            return SecurityGuarantorSerializer(data)

        return  # super(SecuritySerializer, self). to_representation(obj)


class SecuritySharesSerializer(serializers.ModelSerializer):
    security_type = serializers.SerializerMethodField()

    class Meta:
        model = SecurityShares
        exclude = ('polymorphic_ctype',)

    def get_security_type(self, obj):
        return obj.polymorphic_ctype.name


class SecuritySharesPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityShares
        fields = ('number_of_shares', 'share_type', 'loan_application')


class SecuritySavingsSerializer(serializers.ModelSerializer):
    security_type = serializers.SerializerMethodField()

    class Meta:
        model = SecuritySavings
        exclude = ('polymorphic_ctype',)

    def get_security_type(self, obj):
        return obj.polymorphic_ctype.name


class SecuritySavingsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuritySavings
        fields = ('savings_amount', 'loan_application', 'savings_type',)


class SecurityArticleSerializer(serializers.ModelSerializer):
    security_type = serializers.SerializerMethodField()

    class Meta:
        model = SecurityArticle
        exclude = ('polymorphic_ctype',)

    def get_security_type(self, obj):
        return obj.polymorphic_ctype.name


class SecurityArticlePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityArticle
        fields = ('name', 'type', 'identification_type', 'identification', 'description', 'loan_application', 'value',)


class SecurityGuarantorSerializer(serializers.ModelSerializer):
    security_type = serializers.SerializerMethodField()

    class Meta:
        model = SecurityGuarantor
        exclude = ('polymorphic_ctype',)

    def get_security_type(self, obj):
        return obj.polymorphic_ctype.name


class SecurityGuarantorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityGuarantor
        fields = ('guarantor', 'number_of_shares', 'share_type', 'description', 'loan_application',)
