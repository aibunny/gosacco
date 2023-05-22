from django.contrib.auth.models import User
from django.db.models import *
from django.db import models

class Member(Model):
    user = OneToOneField(User,on_delete=models.CASCADE)
    phone_number = CharField(max_length=50)
    registration_date = DateField(auto_now_add=True)
    monthly_income = BigIntegerField(blank=True, null=True,)
    occupation = CharField(max_length=50, blank=True, null=True)
    bank = CharField(blank=True, null=True, max_length=100)
    account_number = CharField(blank=True, null=True, max_length=50)
    signature = ImageField(blank=True, null=True,)
    id_type = CharField(blank=True, null=True, max_length=50)
    id_number = CharField(blank=True, null=True, max_length=50)
    address = CharField(max_length=100)
    city = CharField(max_length=50)
    nationality = CharField(max_length=50)
    comments = TextField(blank=True, null=True,)

    def __unicode__(self):
        return self.user.get_full_name()


class Group(Model):
    name = CharField(max_length=100)
    location = CharField(max_length=50)
    address = CharField(max_length=100)
    leader = ForeignKey(Member, related_name='Group Leader',on_delete=models.CASCADE)
    members = ManyToManyField(Member)

    def __unicode__(self):
        return self.name


class NextOfKin(Model):
    member = OneToOneField(Member,on_delete=models.CASCADE)
    name = CharField(max_length=100)
    relationship = CharField(max_length=50)
    phone_number = CharField(max_length=50)
    occupation = CharField(max_length=50)
    comments = CharField(blank=True, null=True, max_length=250)
    address = CharField(max_length=100)
    current_village = CharField(max_length=100)
    current_subcounty = CharField(max_length=100)
    current_district = CharField(max_length=100)
    permanent_village = CharField(max_length=100)
    permanent_subcounty = CharField(max_length=100)
    permanent_district = CharField(max_length=100)
    signature = ImageField()

    def __unicode__(self):
        return self.member.user.username
