# Create your views here.
from django.core.exceptions import ValidationError
from django.http.response import Http404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from loans.models import Loan, LoanApplication, Security, SecurityShares, SecuritySavings, SecurityArticle, \
    SecurityGuarantor
from loans.serializers import SecuritySerializer, LoanApplicationSerializer, LoanSerializer, \
    SecuritySharesPostSerializer, SecuritySharesSerializer, SecuritySavingsPostSerializer, SecuritySavingsSerializer, \
    SecurityArticleSerializer, SecurityArticlePostSerializer, SecurityGuarantorSerializer, \
    SecurityGuarantorPostSerializer, LoanApplicationPostSerializer
from members.models import Member
from members.permissions import IsOwnerOrAdmin


class LoansView(APIView):
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
        List all of a Member's Loans
        """
        if pk is not None:
            member = self.get_member(int(pk))
        else:
            member = None
        self.check_object_permissions(request, member)
        loans = Loan.get_members_loans(member)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)


class LoanApplicationView(APIView):
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
        List Member's Loan Applications
        """
        if pk is not None:
            member = self.get_member(int(pk))
        else:
            member = None
        self.check_object_permissions(request, member)
        applications = LoanApplication.get_members_loan_applications(member)
        serializer = LoanApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        """
        Add a new Loan Application
        ---
        serializer: loans.serializers.LoanApplicationPostSerializer
        """
        member = self.get_member(int(pk))
        self.check_object_permissions(request, member)
        serializer = LoanApplicationPostSerializer(data=request.data)
        if serializer.is_valid():
            application = LoanApplication.make_loan_application(loan_type=serializer.validated_data['loan_type'],
                                                                member=member,
                                                                amount=serializer.validated_data['amount'],
                                                                payment_period=serializer.validated_data[
                                                                    'payment_period'],
                                                                application_number=serializer.validated_data[
                                                                    'application_number'],
                                                                security_details=serializer.validated_data[
                                                                    'security_details'],
                                                                purpose=serializer.validated_data['purpose'])
            if isinstance(application, LoanApplication):
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif isinstance(application, ValidationError):
                return Response(application, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SecurityView(APIView):
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
        List Member's Securities
        ---
        serializer: loans.serializers.SecuritySerializer
        """
        if pk is not None:
            member = self.get_member(int(pk))
        else:
            member = None
        self.check_object_permissions(request, member)
        securities = Security.get_members_securities(member)
        serializer = SecuritySerializer(securities, many=True)
        return Response(serializer.data)


class LoanSecuritySharesView(APIView):
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
        List Securities in form of shares
        ---
        serializer: loans.serializers.SecuritySharesSerializer
        """
        if pk is not None:
            member = self.get_member(int(pk))
        else:
            member = None
        self.check_object_permissions(request, member)
        security = SecurityShares.get_members_securities(member=member)
        serializer = SecuritySharesSerializer(security, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        """
        Add a new security in form of shares
        ---
        serializer: loans.serializers.SecuritySharesPostSerializer
        """
        member = self.get_member(int(pk))
        self.check_object_permissions(request, member)
        serializer = SecuritySharesPostSerializer(data=request.data)
        if serializer.is_valid():
            new_security = SecurityShares.add_security(loan_application=serializer.validated_data['loan_application'],
                                                       member=member,
                                                       number_of_shares=serializer.validated_data['number_of_shares'],
                                                       share_type=serializer.validated_data['share_type'], )
            if isinstance(new_security, Security):
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif isinstance(new_security, ValidationError):
                return Response(new_security, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanSecuritySavingsView(APIView):
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
        List Securities in form of savings
        ---
        serializer: loans.serializers.SecuritySavingsSerializer
        """
        if pk is not None:
            member = self.get_member(int(pk))
        else:
            member = None
        self.check_object_permissions(request, member)
        security = SecuritySavings.get_members_securities(member=member)
        serializer = SecuritySavingsSerializer(security, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        """
        Add a new security in form of savings
        ---
        serializer: loans.serializers.SecuritySavingsPostSerializer
        """
        member = self.get_member(int(pk))
        self.check_object_permissions(request, member)
        serializer = SecuritySavingsPostSerializer(data=request.data)
        if serializer.is_valid():
            new_security = SecuritySavings.add_security(loan_application=serializer.validated_data['loan_application'],
                                                        member=member,
                                                        savings_amount=serializer.validated_data['savings_amount'],
                                                        savings_type=serializer.validated_data['savings_type'], )
            if isinstance(new_security, Security):
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif isinstance(new_security, ValidationError):
                return Response(new_security, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanSecurityArticlesView(APIView):
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
        List Securities which are physical items
        ---
        serializer: loans.serializers.SecurityArticleSerializer
        """
        if pk is not None:
            member = self.get_member(int(pk))
        else:
            member = None
        self.check_object_permissions(request, member)
        security = SecurityArticle.get_members_securities(member=member)
        serializer = SecurityArticleSerializer(security, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        """
        Add a new security in form of savings
        ---
        serializer: loans.serializers.SecurityArticlePostSerializer
        """
        member = self.get_member(int(pk))
        self.check_object_permissions(request, member)
        serializer = SecurityArticlePostSerializer(data=request.data)
        if serializer.is_valid():
            new_security = SecurityArticle.add_security(loan_application=serializer.validated_data['loan_application'],
                                                        member=member,
                                                        name=serializer.validated_data['name'],
                                                        type=serializer.validated_data['type'],
                                                        identification=serializer.validated_data['identification'],
                                                        identification_type=serializer.validated_data[
                                                            'identification_type'],
                                                        description=serializer.validated_data['description'],
                                                        value=serializer.validated_data['value'], )
            if isinstance(new_security, Security):
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif isinstance(new_security, ValidationError):
                return Response(new_security, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanSecurityGuarantorsView(APIView):
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
        List Securities in form Guarantors savings
        ---
        serializer: loans.serializers.SecurityGuarantorSerializer
        """
        if pk is not None:
            member = self.get_member(int(pk))
        else:
            member = None
        self.check_object_permissions(request, member)
        security = SecurityGuarantor.get_members_securities(member=member)
        serializer = SecurityGuarantorSerializer(security, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        """
        Add a new security in form of savings
        ---
        serializer: loans.serializers.SecurityGuarantorPostSerializer
        """
        member = self.get_member(int(pk))
        self.check_object_permissions(request, member)
        serializer = SecurityGuarantorPostSerializer(data=request.data)
        if serializer.is_valid():
            new_security = SecurityGuarantor.add_security(
                loan_application=serializer.validated_data['loan_application'],
                member=member,
                guarantor=serializer.validated_data['guarantor'],
                number_of_shares=serializer.validated_data['number_of_shares'],
                share_type=serializer.validated_data['share_type'],
                description=serializer.validated_data['description'])
            if isinstance(new_security, Security):
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif isinstance(new_security, ValidationError):
                return Response(new_security, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
