# Create your tests here.
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from loans.models import LoanApplication, LoanType, Security, SecuritySavings
from members.models import Member
from savings.models import SavingsType, Savings


class LoansModelsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="fish", password="fhsdiauf")
        self.user2 = User.objects.create(username="bongo", password="fhsdiJFIDSNFud")
        self.member1 = Member.objects.create(user=self.user1,
                                             phone_number="445465",
                                             registration_date="2015-12-15",
                                             monthly_income="448824",
                                             occupation="Fish",
                                             bank="DFCU",
                                             account_number="78514",
                                             signature="",
                                             id_type="Driving Permit",
                                             id_number="7654",
                                             address="Wano",
                                             city="KLA",
                                             nationality="Ug",
                                             comments="Bongo",
                                             )
        self.member2 = Member.objects.create(user=self.user2,
                                             phone_number="445465",
                                             registration_date="2015-12-15",
                                             monthly_income="448824",
                                             occupation="Fish",
                                             bank="Centenary",
                                             account_number="78s514",
                                             signature="",
                                             id_type="National ID",
                                             id_number="7654354654",
                                             address="Wano si wa ",
                                             city="Wakiso",
                                             nationality="Ug",
                                             comments="Bongo huh",
                                             )

        self.loan_type1 = LoanType.objects.create(
            name="Short term",
            interest=0,
            interest_period=LoanType.YEAR,
            processing_period=5,
            minimum_amount=1000,
            maximum_amount=100000,
            minimum_membership_period=5,  # months
            minimum_shares=12,
            minimum_savings=5,
            minimum_payback_period=120,
            maximum_payback_period=100,
        )

        self.savingType1 = SavingsType.objects.create(name="Annual",
                                                      compulsory=True,
                                                      interval=SavingsType.MONTH,
                                                      minimum_amount=20000,
                                                      maximum_amount=100000,
                                                      interest=1,
                                                      )
        self.savings1 = Savings.objects.create(member=self.member1,
    amount = 100000,
    savings_type = self.savingType1,

        )

        self.loan_application1 = LoanApplication.objects.create(
    application_number = "fsdf34234",
    member = self.member1,
    application_date = "2015-12-15",
    amount = 899,
    purpose = "UHIH IUBHISA",
    payment_period = 60,
    loan_type = self.loan_type1,
    security_details = "fsgdfsgd",
    comment = "sdfsdffsd",
        )

        self.savings_security1 = SecuritySavings.objects.create(
            savings_type=self.savingType1,
            savings_amount=5000,
            loan_application=self.loan_application1,

        )

    def test_total_security_value(self):
        self.assertEquals(self.loan_application1.total_security_value(), 5000)

    def test_is_security_sufficient(self):
        self.assertEquals(self.loan_application1.is_security_sufficient(), True)