# Create your models here.
from django.db.models import Model, CharField, IntegerField, ForeignKey, DateTimeField
from members.models import Member
from django.db import models

class Fee(Model):
    pass

class FeeType(Model):
    name = CharField(max_length=50)
    purpose = CharField(max_length=50)
    minimum_amount = IntegerField()
    maximum_amount = IntegerField()

    def __unicode__(self):
        return self.name


class FeePayment(Model):
    member = ForeignKey(Member,on_delete=models.CASCADE)
    fee_type = ForeignKey(FeeType,on_delete=models.CASCADE)
    date = DateTimeField()
    amount = IntegerField()
    reason = CharField(max_length=250)

    def __unicode__(self):
        return str(self.member)
