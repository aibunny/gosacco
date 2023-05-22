# Create your tests here.
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.test import TestCase

from members.models import Member, Group
from shares.models import Shares, ShareType, SharePurchase, ShareTransfer


class SharesModelsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="fish", password="fhsdiauf")
        self.user2 = User.objects.create(username="bongo", password="fhsdiJFIDSNFud")
        self.user3 = User.objects.create(username="mark", password="IUYGVT678434")
        self.shareType1 = ShareType.objects.create(share_class="A",
                                                   share_price=10000,
                                                   minimum_shares=0,
                                                   maximum_shares=5000,
                                                   )
        self.shareType2 = ShareType.objects.create(share_class="B",
                                                   share_price=12000,
                                                   minimum_shares=10,
                                                   maximum_shares=500,
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
        self.share1 = Shares.objects.create(member=self.member1,
                                            number_of_shares=5,
                                            date="2014-12-12",
                                            share_type=self.shareType1,
                                            )
        self.share2 = Shares.objects.create(member=self.member1,
                                            number_of_shares=4,
                                            date="2014-01-12",
                                            share_type=self.shareType2,
                                            )
        self.share3 = Shares.objects.create(member=self.member2,
                                            number_of_shares=4,
                                            date="2014-01-12",
                                            share_type=self.shareType1,
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

    def test_get_members_shares(self):
        shares = Shares.get_members_shares(self.member1)
        self.assertSequenceEqual(shares, [self.share1, self.share2])

    def test_get_members_shares_with_sharetype(self):
        shares = Shares.get_members_shares(self.member1, self.shareType1)
        self.assertSequenceEqual(shares, [self.share1])

    def test_issue_shares(self):
        shares = 10
        all_shares_before_purchase = Shares.get_members_shares(self.member1, self.shareType1)
        shares_before_purchase = all_shares_before_purchase[0]
        SharePurchase.issue_shares(self.member1, shares, self.shareType1)
        all_shares_after_purchase = Shares.get_members_shares(self.member1, self.shareType1)
        shares_after_purchase = all_shares_after_purchase[0]
        all_purchases = SharePurchase.objects.all()
        purchase = all_purchases[0]
        self.assertEquals(shares, purchase.number_of_shares)
        self.assertEquals(shares_after_purchase.number_of_shares,
                          purchase.number_of_shares + shares_before_purchase.number_of_shares)

    def test_transfer_shares(self):
        new_shares = 3
        sellers_shares_before = Shares.get_members_shares(self.member1, self.shareType1)[0]
        buyers_shares_before = Shares.get_members_shares(self.member2, self.shareType1)[0]

        ShareTransfer.transfer_shares(self.member1, self.member2, new_shares, self.shareType1)

        sellers_shares_after = Shares.get_members_shares(self.member1, self.shareType1)[0]
        buyers_shares_after = Shares.get_members_shares(self.member2, self.shareType1)[0]

        self.assertEquals(sellers_shares_after.number_of_shares, sellers_shares_before.number_of_shares - new_shares)
        self.assertEquals(buyers_shares_after.number_of_shares, buyers_shares_before.number_of_shares + new_shares)

    def test_transfer_shares_excess(self):
        new_shares = 10
        sellers_shares_before = Shares.get_members_shares(self.member1, self.shareType1)[0]
        buyers_shares_before = Shares.get_members_shares(self.member2, self.shareType1)[0]

        ShareTransfer.transfer_shares(self.member1, self.member2, new_shares, self.shareType1)

        sellers_shares_after = Shares.get_members_shares(self.member1, self.shareType1)[0]
        buyers_shares_after = Shares.get_members_shares(self.member2, self.shareType1)[0]

        self.assertEquals(sellers_shares_after.number_of_shares, sellers_shares_before.number_of_shares)
        self.assertEquals(buyers_shares_after.number_of_shares, buyers_shares_before.number_of_shares)

    def test_transfer_shares_seller_without_shares(self):
        new_shares = 2
        share_transfers_before = ShareTransfer.objects.all()

        ShareTransfer.transfer_shares(self.member2, self.member1, new_shares, self.shareType2)
        share_transfers_after = ShareTransfer.objects.all()

        self.assertSequenceEqual(Shares.get_members_shares(self.member2, self.shareType2), [])
        # self.assertSequenceEqual(share_transfers_before, share_transfers_after)


    """
    Shares without sharetypes
    """
    def test_get_shares_no_member_no_sharetype(self):
        shares = Shares.get_shares()
        self.assertSequenceEqual(shares, [self.share1, self.share2, self.share3])

    def test_get_shares_with_member_no_sharetype(self):
        shares = Shares.get_shares(members=self.member2)
        self.assertSequenceEqual(shares, [self.share3])

    def test_get_shares_with_list_no_sharetype(self):
        shares = Shares.get_shares(members=[self.member1, self.member2])
        self.assertSequenceEqual(shares, [self.share1, self.share2, self.share3])

    def test_get_shares_with_list_no_sharetype2(self):
        shares = Shares.get_shares(members=[self.member2])
        self.assertSequenceEqual(shares, [self.share3])

    def test_get_shares_group_no_sharetype(self):
        shares = Shares.get_shares(members=self.group1)
        self.assertSequenceEqual(shares, [self.share1, self.share2])

    """
    Shares with sharetypes
    """

    def test_get_shares_no_member_with_sharetype(self):
        shares = Shares.get_shares(current_share_type=self.shareType1)
        self.assertSequenceEqual(shares, [self.share1, self.share3])

    def test_get_shares_with_member_with_sharetype(self):
        shares = Shares.get_shares(members=self.member1, current_share_type=self.shareType1)
        self.assertSequenceEqual(shares, [self.share1])

    def test_get_shares_with_member_with_sharetype2(self):
        shares = Shares.get_shares(members=self.member1, current_share_type=self.shareType2)
        self.assertSequenceEqual(shares, [self.share2])

    def test_get_shares_with_list_with_sharetype(self):
        shares = Shares.get_shares(members=[self.member1, self.member2], current_share_type=self.shareType1)
        self.assertSequenceEqual(shares, [self.share1, self.share3])

    def test_get_shares_with_list_with_sharetype2(self):
        shares = Shares.get_shares(members=[self.member1, self.member2], current_share_type=self.shareType2)
        self.assertSequenceEqual(shares, [self.share2])

    def test_get_shares_group_with_sharetype(self):
        shares = Shares.get_shares(members=self.group1, current_share_type=self.shareType1)
        self.assertSequenceEqual(shares, [self.share1])

    """
    SharePurchases without sharetypes
    """

    def test_get_share_purchases_no_member_no_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)
        purchase_list = SharePurchase.objects.filter()
        purchased_shares = SharePurchase.get_share_purchases()
        self.assertItemsEqual(purchased_shares, purchase_list)

    def test_get_share_purchases_with_member_no_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)
        purchase_list = SharePurchase.objects.filter(member=self.member1)
        purchased_shares = SharePurchase.get_share_purchases(members=self.member1)
        self.assertItemsEqual(purchased_shares, purchase_list)

    def test_get_share_purchases_with_group_no_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)
        member= Member.objects.filter(group__pk=self.group1.pk)
        purchase_list = SharePurchase.objects.filter(member=member)
        purchased_shares = SharePurchase.get_share_purchases(members=self.group1)
        self.assertItemsEqual(purchased_shares, purchase_list)

    def test_get_share_purchases_with_list_no_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)
        purchase_list = SharePurchase.objects.filter(member=self.member2)
        purchased_shares = SharePurchase.get_share_purchases(members=[self.member2])
        self.assertItemsEqual(purchased_shares, purchase_list)

    """
    SharePurchases with sharetypes
    """

    def test_get_share_purchases_no_member_with_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)
        purchase_list = SharePurchase.objects.filter(share_type=self.shareType1)
        purchased_shares = SharePurchase.get_share_purchases(current_share_type=self.shareType1)
        self.assertItemsEqual(purchased_shares, purchase_list)

    def test_get_share_purchases_with_member_with_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)
        purchase_list = SharePurchase.objects.filter(member=self.member1, share_type=self.shareType1)
        purchased_shares = SharePurchase.get_share_purchases(members=self.member1, current_share_type=self.shareType1)
        self.assertItemsEqual(purchased_shares, purchase_list)

    def test_get_share_purchases_with_group_with_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)
        member= Member.objects.filter(group__pk=self.group1.pk)
        purchase_list = SharePurchase.objects.filter(member=member, share_type=self.shareType1)
        purchased_shares = SharePurchase.get_share_purchases(members=self.group1, current_share_type=self.shareType1)
        self.assertItemsEqual(purchased_shares, purchase_list)

    def test_get_share_purchases_with_list_with_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)
        purchase_list = SharePurchase.objects.filter(member=self.member2, share_type=self.shareType1)
        purchased_shares = SharePurchase.get_share_purchases(members=[self.member2], current_share_type=self.shareType1)
        self.assertItemsEqual(purchased_shares, purchase_list)





    """
    ShareTransfers without sharetypes
    """
    def test_get_share_transfers(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)

        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member1, number_of_shares=11, share_type=self.shareType1)
        transferred_list = ShareTransfer.objects.all()
        transferred_share = ShareTransfer.get_share_transfers()

        self.assertItemsEqual(transferred_share, transferred_list)

    def test_get_share_transfers_with_member_no_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)

        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member1, number_of_shares=11, share_type=self.shareType1)
        transferred_list = ShareTransfer.objects.filter(Q(seller=self.member1) | Q(buyer=self.member1))
        transferred_share = ShareTransfer.get_share_transfers(members=self.member1)

        self.assertItemsEqual(transferred_share, transferred_list)

    def test_get_share_transfer_with_group_no_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)

        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member1, number_of_shares=11, share_type=self.shareType1)
        ShareTransfer.transfer_shares(seller=self.member1, buyer=self.member2, number_of_shares=2, share_type=self.shareType1)
        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member3, number_of_shares=3, share_type=self.shareType2)
        group_members = Member.objects.filter(group__id=self.group3.pk)
        transferred_list = ShareTransfer.objects.filter(Q(buyer__in=group_members) | Q(seller__in=group_members))
        transferred_share = ShareTransfer.get_share_transfers(members=self.group3)
        self.assertItemsEqual(transferred_share, transferred_list)

    def test_get_share_transfers_with_list_no_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)

        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member1, number_of_shares=11, share_type=self.shareType1)
        ShareTransfer.transfer_shares(seller=self.member1, buyer=self.member2, number_of_shares=2, share_type=self.shareType1)
        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member3, number_of_shares=3, share_type=self.shareType2)
        group_members = [self.member1, self.member3]
        transferred_list = ShareTransfer.objects.filter(Q(buyer__in=group_members) | Q(seller__in=group_members))
        transferred_share = ShareTransfer.get_share_transfers(members=group_members)
        self.assertItemsEqual(transferred_share, transferred_list)

    """
    ShareTransfers with sharetypes
    """
    def test_get_share_transfers_with_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)

        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member1, number_of_shares=11, share_type=self.shareType1)
        ShareTransfer.transfer_shares(seller=self.member1, buyer=self.member2, number_of_shares=2, share_type=self.shareType1)
        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member3, number_of_shares=3, share_type=self.shareType2)
        transferred_list = ShareTransfer.objects.filter(share_type=self.shareType1)
        transferred_share = ShareTransfer.get_share_transfers(current_share_type=self.shareType1)
        self.assertItemsEqual(transferred_share, transferred_list)

    def test_get_share_transfers_with_member_with_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)

        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member1, number_of_shares=11, share_type=self.shareType1)
        ShareTransfer.transfer_shares(seller=self.member1, buyer=self.member2, number_of_shares=2, share_type=self.shareType1)
        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member3, number_of_shares=3, share_type=self.shareType2)
        member = self.member3
        transferred_list = ShareTransfer.objects.filter(Q(seller=member) | Q(buyer=member), share_type=self.shareType1)
        transferred_share = ShareTransfer.get_share_transfers(members=member, current_share_type=self.shareType1)
        self.assertItemsEqual(transferred_share, transferred_list)

    def test_get_share_transfer_with_group_with_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)

        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member1, number_of_shares=11, share_type=self.shareType1)
        ShareTransfer.transfer_shares(seller=self.member1, buyer=self.member2, number_of_shares=2, share_type=self.shareType1)
        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member3, number_of_shares=3, share_type=self.shareType2)
        group_members = Member.objects.filter(group__id=self.group1.pk)
        transferred_list = ShareTransfer.objects.filter(Q(buyer__in=group_members) | Q(seller__in=group_members), share_type=self.shareType2)
        transferred_share = ShareTransfer.get_share_transfers(members=self.group1, current_share_type=self.shareType2)
        self.assertItemsEqual(transferred_share, transferred_list)

    def test_get_share_transfers_with_list_with_sharetype(self):
        SharePurchase.issue_shares(member=self.member1, shares=3, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member2, shares=15, share_type=self.shareType2)
        SharePurchase.issue_shares(member=self.member2, shares=67, share_type=self.shareType1)
        SharePurchase.issue_shares(member=self.member1, shares=1, share_type=self.shareType1)

        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member1, number_of_shares=11, share_type=self.shareType1)
        ShareTransfer.transfer_shares(seller=self.member1, buyer=self.member2, number_of_shares=2, share_type=self.shareType1)
        ShareTransfer.transfer_shares(seller=self.member2, buyer=self.member3, number_of_shares=3, share_type=self.shareType2)
        group_members = [self.member1, self.member3]
        transferred_list = ShareTransfer.objects.filter(Q(buyer__in=group_members) | Q(seller__in=group_members), share_type=self.shareType2)
        transferred_share = ShareTransfer.get_share_transfers(members=group_members, current_share_type=self.shareType2)
        print transferred_list
        print transferred_share
        self.assertItemsEqual(transferred_share, transferred_list)

