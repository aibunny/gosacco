# Create your models here.
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db.models import Model, FloatField, ForeignKey, DateField, BigIntegerField, IntegerField, ManyToManyField, \
    CharField, TextField, DateTimeField, OneToOneField, Sum, BooleanField
from django.utils.timezone import now
from notifications.signals import notify
from django.db import models
from polymorphic.models import PolymorphicModel

from members.models import Member
from savings.models import SavingsType, Savings
from shares.models import Shares, ShareType


class LoanType(Model):
    YEAR = 'year'
    MONTH = 'month'
    DAY = 'day'
    INTEREST_PERIOD_CHOICES = (
        (YEAR, 'per anum'),
        (MONTH, 'per month'),
        (DAY, 'per day'),
    )
    name = CharField(max_length=50)
    interest = FloatField()
    interest_period = CharField(max_length=50, choices=INTEREST_PERIOD_CHOICES, default=YEAR)
    processing_period = IntegerField(help_text="In days")
    minimum_amount = BigIntegerField()
    maximum_amount = BigIntegerField()
    minimum_membership_period = IntegerField(help_text="In months(A month is 30 days)")  # months
    minimum_shares = BigIntegerField()
    minimum_savings = BigIntegerField()
    minimum_payback_period = IntegerField(help_text="In days")
    maximum_payback_period = IntegerField(help_text="In days")

    @classmethod
    def get_loan_types(cls):
        loan_types = cls.objects.filter()
        return loan_types

    def __unicode__(self):
        return self.name


class LoanApplication(Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )
    application_number = CharField(max_length=100)
    member = ForeignKey(Member,on_delete=models.CASCADE)
    application_date = DateField(auto_now_add=True)
    amount = BigIntegerField()
    purpose = CharField(max_length=250, help_text="Purpose for the loan")
    payment_period = IntegerField(help_text="In Days")
    loan_type = ForeignKey(LoanType, related_name="LoanType",on_delete=models.CASCADE)
    status = CharField(max_length=25, choices=STATUS_CHOICES, default=PENDING,
                       help_text="Current status of the application")
    security_details = TextField(help_text="Basic info provided about the security")
    security_satisfied = BooleanField(default=False)
    comment = TextField(blank=True, null=True, help_text="Feedback from management")

    def approve_loan_application(self, approver):
        if self.security_satisfied:
            self.status = self.APPROVED
            self.save()
            notify.send(approver.member, recipient=self.member.user, verb='approved',
            description='Your loan application was approved', target=self, level='success')
            return True
        else:
            return False

    def reject_loan_application(self, rejecter, comment=None):
        self.status = self.REJECTED
        self.save()
        notify.send(rejecter.member, recipient=self.member.user, verb='rejected',
            description='Your loan application was rejected', target=self, level='fail')
        if comment:
            self.give_feedback_on_loan_application(comment=comment)

    def give_feedback_on_loan_application(self, comment):
        self.comment = comment

    @classmethod
    def make_loan_application(cls, application_number, amount, purpose, payment_period, security_details, member,
                              loan_type):
        application = cls(application_number=application_number, amount=amount, purpose=purpose,
                          payment_period=payment_period, security_details=security_details, member=member,
                          loan_type=loan_type)
        errors = application.meets_requirements()
        if application.valid is False:
            return ValidationError(errors)
        application.save()
        return application

    @classmethod
    def get_members_loan_applications(cls, member, loan_type=None):
        if loan_type is None:
            loans = cls.objects.filter(member=member)
        else:
            loans = cls.objects.filter(member=member, loan_type=loan_type)

        return loans

    valid = False

    def meets_requirements(self):
        self.valid = True
        errors = []
        if self.amount < self.loan_type.minimum_amount:
            self.valid = False
            error = 'The minimum amount you can ask for is %d' % self.loan_type.minimum_amount
            errors.append(error)

        if self.amount > self.loan_type.maximum_amount:
            self.valid = False
            error = 'The maximum amount you can ask for is %d' % self.loan_type.maximum_amount
            errors.append(error)

        membership_period = now().date() - self.member.registration_date
        if membership_period < timedelta(self.loan_type.minimum_membership_period * 30):
            self.valid = False
            error = 'You must be a member for at least %d months to be eligible' % self.loan_type.minimum_membership_period
            errors.append(error)

        if self.payment_period < self.loan_type.minimum_payback_period:
            self.valid = False
            error = 'This loan must be paid in more than %d days' % self.loan_type.minimum_payback_period
            errors.append(error)

        if self.payment_period > self.loan_type.maximum_payback_period:
            self.valid = False
            error = 'This loan must be paid in less than %d days' % self.loan_type.maximum_payback_period
            errors.append(error)

        if Savings.get_members_savings_total(self.member) < self.loan_type.minimum_savings:
            self.valid = False
            error = 'You must have at least a total of %d savings to qualify for this loan' % self.loan_type.minimum_savings
            errors.append(error)

        if Shares.get_members_shares_total(self.member) < self.loan_type.minimum_shares:
            self.valid = False
            error = 'You must have at least a total of %d shares to qualify for this loan' % self.loan_type.minimum_shares
            errors.append(error)
        savings_rules = LoanRuleSavings.objects.filter(loan_type=self.loan_type)
        shares_rules = LoanRuleShares.objects.filter(loan_type=self.loan_type)
        other_rules = LoanRuleOther.objects.filter(loan_type=self.loan_type)

        for rule in shares_rules:
            try:
                current_shares = Shares.get_members_shares(self.member, rule.shares_type)[0].number_of_shares
                if current_shares < rule.minimum:
                    self.valid = False
                    error = 'You need to have at least %s class %s shares to qualify for this loan' % (
                        rule.minimum, rule.shares_type)
                    errors.append(error)
                if current_shares > rule.maximum != 0:
                    self.valid = False
                    error = 'You need to have at most %s class %s shares to qualify for this loan' % (
                        rule.maximum, rule.shares_type)
                    errors.append(error)

            except IndexError:
                self.valid = False
                error = 'You need to have at least %s class %s shares to qualify for this loan' % (
                    rule.minimum, rule.shares_type)
                errors.append(error)

        for rule in savings_rules:
            try:
                current_savings = Savings.get_members_savings(self.member, rule.savings_type)[0].amount
                if current_savings < rule.minimum:
                    self.valid = False
                    error = 'You need to have at least %s %s savings to qualify for this loan' % (
                        rule.minimum, rule.savings_type)
                    errors.append(error)
                if current_savings > rule.maximum != 0:
                    self.valid = False
                    error = 'You need to have at most %s %s savings to qualify for this loan' % (
                        rule.maximum, rule.savings_type)
                    errors.append(error)
            except IndexError:
                self.valid = False
                error = 'You need to have at least %s %s savings to qualify for this loan' % (
                    rule.minimum, rule.savings_type)
                errors.append(error)
        self.security_satisfied = self.is_security_sufficient()
        #print self.security_satisfied
        # if self.is_security_sufficient():
        #     print("security is sufficient")
        #     print(self.is_security_sufficient())
        #     self.security_satisfied = True
        #     #TODO Check that the value of of shares is not None and print 0 if it is.
        #     error = 'Your total securities value(%s) is less that what you are requesting for(%s)' % (
        #         self.total_security_value(), self.amount)
        #     errors.append(error)

        return errors

    def total_security_value(self):
        all_securites = Security.objects.filter(loan_application=self).aggregate(total_value=Sum('value'))
        return all_securites['total_value']

    def is_security_sufficient(self):
        return self.amount <= self.total_security_value()

    def clean(self):
        errors = self.meets_requirements()
        if self.valid is False:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.security_satisfied = self.is_security_sufficient()
        super(LoanApplication, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.loan_type.__unicode__()+" loan: "+self.application_number

    @classmethod
    def view_loan_applications(cls, member=None, ):
        pass


class Loan(Model):
    application = ForeignKey(LoanApplication,on_delete=models.CASCADE)
    member = ForeignKey(Member,on_delete=models.CASCADE)
    approval_date = DateTimeField()
    amount = BigIntegerField(help_text="Actual amount approved")
    payment_period = IntegerField(help_text="In days")
    loan_type = ForeignKey(LoanType,on_delete=models.CASCADE)
    security_details = TextField(help_text="Basic info provided about the security")

    @classmethod
    def get_members_loans(cls, member, loan_type=None):
        if loan_type is None:
            loans = cls.objects.filter(member=member)
        else:
            loans = cls.objects.filter(member=member, loan_type=loan_type)

        return loans

    def __unicode__(self):
        return self.member.user.username


class LoanRuleSavings(Model):
    loan_type = ForeignKey(LoanType, related_name='savings_rules',on_delete=models.CASCADE)
    savings_type = ForeignKey(SavingsType, blank=True, null=True,on_delete=models.CASCADE)
    minimum = BigIntegerField()
    maximum = BigIntegerField()


class LoanRuleShares(Model):
    loan_type = ForeignKey(LoanType, related_name='shares_rules',on_delete=models.CASCADE)
    shares_type = ForeignKey(ShareType, blank=True, null=True,on_delete=models.CASCADE)
    minimum = BigIntegerField()
    maximum = BigIntegerField()


class LoanRuleOther(Model):
    loan_type = ForeignKey(LoanType,related_name='extra_rules', on_delete=models.CASCADE)
    rule = CharField(max_length=500)


class Security(PolymorphicModel):
    loan_application = ForeignKey(LoanApplication,on_delete=models.CASCADE)
    loan = ForeignKey(Loan, blank=True, null=True,on_delete=models.CASCADE)
    value = BigIntegerField()

    @classmethod
    def get_members_securities(cls, member):
        securities = cls.objects.filter(loan_application__member=member)
        return securities

    @classmethod
    def add_security(cls, loan_application, member):
        pass

    def save(self, *args, **kwargs):
        self.loan_application.security_satisfied = self.loan_application.is_security_sufficient()
        super(Security, self).save(*args, **kwargs)
        self.loan_application.save()

    def delete(self, *args, **kwargs):
        self.loan_application.security_satisfied = self.loan_application.is_security_sufficient()
        super(Security, self).delete(*args, **kwargs)
        self.loan_application.save()


class SecurityShares(Security):
    number_of_shares = IntegerField()
    share_type = ForeignKey(ShareType,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Security shares"

    @classmethod
    def add_security(cls, loan_application, member, number_of_shares, share_type):

        security = cls(loan_application=loan_application, number_of_shares=number_of_shares, share_type=share_type)
        if member != loan_application.member:
            return ValidationError(
                {"loan_application": "Invalid Loan Application"})
        try:
            available_shares = Shares.objects.get(share_type=share_type, member=loan_application.member)
        except Shares.DoesNotExist:
            return ValidationError(
                {"number_of_shares": "You don't have any shares of class " + share_type.__str__()})

        if available_shares.number_of_shares < number_of_shares:
            return ValidationError(
                {"number_of_shares": "You don't have enough shares of class " + share_type.__str__()})
        security.save()
        return security

    def save(self, *args, **kwargs):
        self.value = self.share_value()
        super(SecurityShares, self).save(*args, **kwargs)

    def share_value(self):
        return self.number_of_shares * self.share_type.share_price

    def clean(self):
        try:
            available_shares = Shares.objects.get(share_type=self.share_type, member=self.loan_application.member)
        except Shares.DoesNotExist:
            raise ValidationError(
                {"number_of_shares": "You don't have any shares of class " + self.share_type.__str__()})

        if available_shares.number_of_shares < self.number_of_shares:
            raise ValidationError(
                {"number_of_shares": "You don't have enough shares of class " + self.share_type.__str__()})

    def __unicode__(self):
        return str(self.number_of_shares) + " " + str(self.share_type) + " shares"


class SecuritySavings(Security):
    savings_type = ForeignKey(SavingsType,on_delete=models.CASCADE)
    savings_amount = BigIntegerField()

    @classmethod
    def add_security(cls, loan_application, member, savings_amount, savings_type):
        if member != loan_application.member:
            return ValidationError(
                {"loan_aplication": "Invalid Loan Application"})
        security = cls(loan_application=loan_application, savings_amount=savings_amount, savings_type=savings_type)
        try:
            available_savings = Savings.objects.get(savings_type=savings_type, member=loan_application.member)
        except Savings.DoesNotExist:
            return ValidationError(
                {"savings_amount": "You don't have any savings of type " + savings_type.__str__()})

        if available_savings.amount < savings_amount:
            return ValidationError(
                {"savings_amount": "You don't have enough savings of type " + savings_type.__str__()})
        security.save()
        return security

    def save(self, *args, **kwargs):
        self.value = self.saving_value()
        self.clean()
        super(SecuritySavings, self).save(*args, **kwargs)

    def saving_value(self):
        return self.savings_amount

    def clean(self):
        try:
            available_savings = Savings.objects.get(savings_type=self.savings_type, member=self.loan_application.member)
        except Savings.DoesNotExist:
            raise ValidationError(
                {"savings_amount": "You don't have any savings of type " + self.savings_type.__str__()})

        if available_savings.amount < self.savings_amount:
            raise ValidationError(
                {"savings_amount": "You don't have enough savings of type " + self.savings_type.__str__()})

    def __unicode__(self):
        return str(self.savings_amount) + " " + str(self.savings_type) + " savings"


class SecurityArticle(Security):
    name = CharField(max_length=100)
    type = CharField(max_length=100, help_text="eg Land, car, house")
    identification_type = CharField(max_length=100, help_text="eg Land title, car logbook")
    identification = CharField(max_length=100, help_text="eg ID Number, Title number")
    description = TextField()

    @classmethod
    def add_security(cls, loan_application, member, name, type, identification_type, identification, description,
                     value):
        if member != loan_application.member:
            return ValidationError(
                {"loan_aplication": "Invalid Loan Application"})
        security = cls(loan_application=loan_application, name=name, type=type, identification=identification,
                       identification_type=identification_type, description=description, value=value)
        security.save()
        return security

    def __unicode__(self):
        return self.name


class SecurityGuarantor(Security):
    guarantor = ForeignKey(Member,on_delete=models.CASCADE)
    number_of_shares = IntegerField()
    share_type = ForeignKey(ShareType,on_delete=models.CASCADE)
    description = TextField()

    @classmethod
    def add_security(cls, loan_application, member, guarantor, share_type, number_of_shares, description):
        if member != loan_application.member:
            return ValidationError(
                {"loan_aplication": "Invalid Loan Application"})
        security = cls(loan_application=loan_application, guarantor=guarantor, share_type=share_type,
                       number_of_shares=number_of_shares,
                       description=description)
        security.save()
        return security

    def save(self, *args, **kwargs):
        self.value = self.share_value()
        super(SecurityGuarantor, self).save(*args, **kwargs)

    def share_value(self):
        return self.number_of_shares * self.share_type.share_price

    def __unicode__(self):
        return self.guarantor.user.username
