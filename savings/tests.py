# Create your tests here.
from django.contrib.auth.models import User
from django.db.models import Q
from django.test import TestCase
from django.utils import timezone
from members.models import Member, Group
from savings.models import SavingsType, Savings, SavingsDeposit, SavingsWithdrawal


class SavingsModelsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="fish", password="fhsdiauf")
        self.user2 = User.objects.create(username="bongo", password="fhsdiJFIDSNFud")
        self.user3 = User.objects.create(username="mark", password="IUYGVT678434")
        self.savingType1 = SavingsType.objects.create(name="Annual",
                                                      compulsory=True,
                                                      interval=SavingsType.MONTH,
                                                      minimum_amount=20000,
                                                      maximum_amount=100000,
                                                      interest=1,
                                                      )
        self.savingType2 = SavingsType.objects.create(name="New Office",
                                                      compulsory=False,
                                                      interval=SavingsType.MONTH,
                                                      minimum_amount=1000,
                                                      maximum_amount=0,
                                                      interest=0,
                                                      )
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
        self.member3 = Member.objects.create(user=self.user3,
                                             phone_number="445465",
                                             registration_date="2015-06-05",
                                             monthly_income="448824",
                                             occupation="Goat",
                                             bank="Quali",
                                             account_number="78s514",
                                             signature="",
                                             id_type="National ID",
                                             id_number="7654354654",
                                             address="Wali",
                                             city="Mbarara",
                                             nationality="KE",
                                             comments="Diu",
                                             )

        self.saving1 = Savings.objects.create(member=self.member1,
                                             amount=50000,
                                             date="2014-12-12",
                                             savings_type=self.savingType1,
                                             )
        self.saving2 = Savings.objects.create(member=self.member1,
                                             amount=2500,
                                             date="2014-01-12",
                                             savings_type=self.savingType2,
                                             )
        self.saving3 = Savings.objects.create(member=self.member2,
                                             amount=20000,
                                             date="2014-01-12",
                                             savings_type=self.savingType1,
                                             )

        self.group1 = Group.objects.create(
            name="BOngo",
            location="Kibuli",
            address="P.O.Box 459, Kampala",
            leader=self.member1,

        )
        self.group2 = Group.objects.create(
            name="Fwwaaa",
            location="Kawempe",
            address="P.O.Box 49, Kampala",
            leader=self.member2,

        )
        self.group3 = Group.objects.create(
            name="WEewewer",
            location="Wali",
            address="P.O.Box 449, Kampala",
            leader=self.member3,

        )
        self.group1.members.add(self.member1)
        self.group1.save()
        self.group2.members.add(self.member2)
        self.group2.save()
        self.group3.members.add(self.member3)
        self.group3.save()

    def test_get_members_savings(self):
        savings = Savings.get_members_savings(self.member1)
        self.assertSequenceEqual(savings, [self.saving1, self.saving2])

    def test_get_members_savings_with_savingstype(self):
        savings = Savings.get_members_savings(self.member1, self.savingType1)
        self.assertSequenceEqual(savings, [self.saving1])

    def test_make_savings(self):
        new_savings = 5000
        savings_before = Savings.objects.get(member=self.member1, savings_type=self.savingType1)
        self.assertEqual(savings_before, self.saving1)
        SavingsDeposit.deposit_savings(self.member1, self.savingType1, new_savings, timezone.now())
        savings_after = Savings.objects.get(member=self.member1, savings_type=self.savingType1)
        self.assertEqual(savings_after, self.saving1)
        self.assertEqual(savings_before.amount+new_savings, savings_after.amount)

    #Savings without savingstypes

    def test_get_savings_no_member_no_savingstype(self):
        savings = Savings.get_savings()
        self.assertSequenceEqual(savings, [self.saving1, self.saving2, self.saving3])

    def test_get_savings_with_member_no_savingstype(self):
        savings = Savings.get_savings(members=self.member2)
        self.assertSequenceEqual(savings, [self.saving3])

    def test_get_savings_with_list_no_savingstype(self):
        savings = Savings.get_savings(members=[self.member1, self.member2])
        self.assertSequenceEqual(savings, [self.saving1, self.saving2, self.saving3])

    def test_get_savings_with_list_no_savingstype2(self):
        savings = Savings.get_savings(members=[self.member2])
        self.assertSequenceEqual(savings, [self.saving3])

    def test_get_savings_group_no_savingstype(self):
        savings = Savings.get_savings(members=self.group1)
        self.assertSequenceEqual(savings, [self.saving1, self.saving2])

    #Savings with savingstypes

    def test_get_savings_no_member_with_savingstype(self):
        savings = Savings.get_savings(current_savings_type=self.savingType1)
        self.assertSequenceEqual(savings, [self.saving1, self.saving3])

    def test_get_savings_with_member_with_savingstype(self):
        savings = Savings.get_savings(members=self.member1, current_savings_type=self.savingType1)
        self.assertSequenceEqual(savings, [self.saving1])

    def test_get_savings_with_member_with_savingstype2(self):
        savings = Savings.get_savings(members=self.member1, current_savings_type=self.savingType2)
        self.assertSequenceEqual(savings, [self.saving2])

    def test_get_savings_with_list_with_savingstype(self):
        savings = Savings.get_savings(members=[self.member1, self.member2], current_savings_type=self.savingType1)
        self.assertSequenceEqual(savings, [self.saving1, self.saving3])

    def test_get_savings_with_list_with_savingstype2(self):
        savings = Savings.get_savings(members=[self.member1, self.member2], current_savings_type=self.savingType2)
        self.assertSequenceEqual(savings, [self.saving2])

    def test_get_savings_group_with_savingstype(self):
        savings = Savings.get_savings(members=self.group1, current_savings_type=self.savingType1)
        self.assertSequenceEqual(savings, [self.saving1])

    #SavingsDeposits without savingstypes

    def test_get_savings_deposits_no_member_no_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)
        purchase_list = SavingsDeposit.objects.filter()
        purchased_savings = SavingsDeposit.get_savings_deposits()
        self.assertItemsEqual(purchased_savings, purchase_list)

    def test_get_savings_deposits_with_member_no_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)
        purchase_list = SavingsDeposit.objects.filter(member=self.member1)
        purchased_savings = SavingsDeposit.get_savings_deposits(members=self.member1)
        self.assertItemsEqual(purchased_savings, purchase_list)

    def test_get_savings_deposits_with_group_no_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)
        member= Member.objects.filter(group__pk=self.group1.pk)
        purchase_list = SavingsDeposit.objects.filter(member=member)
        purchased_savings = SavingsDeposit.get_savings_deposits(members=self.group1)
        self.assertItemsEqual(purchased_savings, purchase_list)

    def test_get_savings_deposits_with_list_no_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)
        purchase_list = SavingsDeposit.objects.filter(member=self.member2)
        purchased_savings = SavingsDeposit.get_savings_deposits(members=[self.member2])
        self.assertItemsEqual(purchased_savings, purchase_list)

    #SavingsDeposits with savingstypes

    def test_get_savings_deposits_no_member_with_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)
        purchase_list = SavingsDeposit.objects.filter(savings_type=self.savingType1)
        purchased_savings = SavingsDeposit.get_savings_deposits(current_savings_type=self.savingType1)
        self.assertItemsEqual(purchased_savings, purchase_list)

    def test_get_savings_deposits_with_member_with_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)
        purchase_list = SavingsDeposit.objects.filter(member=self.member1, savings_type=self.savingType1)
        purchased_savings = SavingsDeposit.get_savings_deposits(members=self.member1, current_savings_type=self.savingType1)
        self.assertItemsEqual(purchased_savings, purchase_list)

    def test_get_savings_deposits_with_group_with_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)
        member= Member.objects.filter(group__pk=self.group1.pk)
        purchase_list = SavingsDeposit.objects.filter(member=member, savings_type=self.savingType1)
        purchased_savings = SavingsDeposit.get_savings_deposits(members=self.group1, current_savings_type=self.savingType1)
        self.assertItemsEqual(purchased_savings, purchase_list)

    def test_get_savings_deposits_with_list_with_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)
        purchase_list = SavingsDeposit.objects.filter(member=self.member2, savings_type=self.savingType1)
        purchased_savings = SavingsDeposit.get_savings_deposits(members=[self.member2], current_savings_type=self.savingType1)
        self.assertItemsEqual(purchased_savings, purchase_list)

    #SavingsTransfers without savingstypes

    def test_get_withdrawals(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)

        SavingsWithdrawal.withdraw_savings(member=self.member2, amount=11, savings_type=self.savingType1)
        transferred_list = SavingsWithdrawal.objects.all()
        transferred_savings = SavingsWithdrawal.get_withdrawals()

        self.assertItemsEqual(transferred_savings, transferred_list)

    def test_get_savings_withdrawals_with_member_no_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)

        SavingsWithdrawal.withdraw_savings(member=self.member1, amount=11, savings_type=self.savingType1)
        transferred_list = SavingsWithdrawal.objects.filter(member=self.member1)
        transferred_savings = SavingsWithdrawal.get_withdrawals(members=self.member1)

        self.assertItemsEqual(transferred_savings, transferred_list)

    def test_get_savings_withdrawal_with_group_no_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)

        SavingsWithdrawal.withdraw_savings(member=self.member1, amount=11, savings_type=self.savingType1)
        SavingsWithdrawal.withdraw_savings(member=self.member2, amount=2, savings_type=self.savingType1)
        SavingsWithdrawal.withdraw_savings(member=self.member3, amount=3, savings_type=self.savingType2)
        group_members = Member.objects.filter(group__id=self.group3.pk)
        transferred_list = SavingsWithdrawal.objects.filter(member__in=group_members)
        transferred_savings = SavingsWithdrawal.get_withdrawals(members=self.group3)
        self.assertItemsEqual(transferred_savings, transferred_list)

    def test_get_savings_withdrawals_with_list_no_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)

        SavingsWithdrawal.withdraw_savings(member=self.member1, amount=11, savings_type=self.savingType1)
        SavingsWithdrawal.withdraw_savings(member=self.member2, amount=2, savings_type=self.savingType1)
        SavingsWithdrawal.withdraw_savings(member=self.member3, amount=3, savings_type=self.savingType2)
        group_members = [self.member1, self.member3]
        transferred_list = SavingsWithdrawal.objects.filter(member__in=group_members)
        transferred_savings = SavingsWithdrawal.get_withdrawals(members=group_members)
        self.assertItemsEqual(transferred_savings, transferred_list)

    #SavingsTransfers with savingstypes

    def test_get_savings_withdrawals_with_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)

        SavingsWithdrawal.withdraw_savings(member=self.member1, amount=11, savings_type=self.savingType1)
        SavingsWithdrawal.withdraw_savings(member=self.member2, amount=2, savings_type=self.savingType1)
        SavingsWithdrawal.withdraw_savings(member=self.member3, amount=3, savings_type=self.savingType2)
        transferred_list = SavingsWithdrawal.objects.filter(savings_type=self.savingType1)
        transferred_savings = SavingsWithdrawal.get_withdrawals(current_savings_type=self.savingType1)
        self.assertItemsEqual(transferred_savings, transferred_list)

    def test_get_savings_withdrawals_with_member_with_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)

        SavingsWithdrawal.withdraw_savings(member=self.member1, amount=11, savings_type=self.savingType1)
        SavingsWithdrawal.withdraw_savings(member=self.member2, amount=2, savings_type=self.savingType1)
        SavingsWithdrawal.withdraw_savings(member=self.member3, amount=3, savings_type=self.savingType2)
        member = self.member3
        transferred_list = SavingsWithdrawal.objects.filter(member=member, savings_type=self.savingType1)
        transferred_savings = SavingsWithdrawal.get_withdrawals(members=member, current_savings_type=self.savingType1)
        self.assertItemsEqual(transferred_savings, transferred_list)

    def test_get_savings_withdrawal_with_group_with_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)

        SavingsWithdrawal.withdraw_savings(member=self.member1, amount=11, savings_type=self.savingType1)
        SavingsWithdrawal.withdraw_savings(member=self.member2, amount=2, savings_type=self.savingType1)
        SavingsWithdrawal.withdraw_savings(member=self.member3, amount=3, savings_type=self.savingType2)
        group_members = Member.objects.filter(group__id=self.group1.pk)
        transferred_list = SavingsWithdrawal.objects.filter(member__in=group_members, savings_type=self.savingType2)
        transferred_savings = SavingsWithdrawal.get_withdrawals(members=self.group1, current_savings_type=self.savingType2)
        self.assertItemsEqual(transferred_savings, transferred_list)

    def test_get_savings_withdrawals_with_list_with_savingstype(self):
        SavingsDeposit.deposit_savings(member=self.member1, amount=3, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member2, amount=15, savings_type=self.savingType2)
        SavingsDeposit.deposit_savings(member=self.member2, amount=67, savings_type=self.savingType1)
        SavingsDeposit.deposit_savings(member=self.member1, amount=1, savings_type=self.savingType1)

        SavingsWithdrawal.withdraw_savings(member=self.member1, amount=11, savings_type=self.savingType1)
        SavingsWithdrawal.withdraw_savings(member=self.member2, amount=2, savings_type=self.savingType1)
        SavingsWithdrawal.withdraw_savings(member=self.member1, amount=3, savings_type=self.savingType2)
        group_members = [self.member1, self.member3]
        transferred_list = SavingsWithdrawal.objects.filter(member__in=group_members, savings_type=self.savingType2)
        transferred_savings = SavingsWithdrawal.get_withdrawals(members=group_members, current_savings_type=self.savingType2)
        print transferred_list
        print transferred_savings
        self.assertItemsEqual(transferred_savings, transferred_list)

