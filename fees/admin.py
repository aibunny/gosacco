from django.contrib import admin

# Register your models here.
from fees.models import FeeType, FeePayment


class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'purpose', 'minimum_amount', 'maximum_amount')


class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'fee_type', 'amount', 'date', 'reason')


admin.site.register(FeeType, FeeTypeAdmin)
admin.site.register(FeePayment, FeePaymentAdmin)
