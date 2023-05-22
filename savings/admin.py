# Register your models here.
from django.contrib import admin


class SavingsAdmin(admin.ModelAdmin):
    list_display = ('member', 'savings_type', 'amount', 'date')
    readonly_fields = ('member', 'savings_type', 'amount', 'date')


class SavingsWithdrawalAdmin(admin.ModelAdmin):
    list_display = ('member', 'savings_type', 'amount', 'date')

    def save_model(self, request, obj, form, change):
        SavingsWithdrawal.withdraw_savings(obj.member, obj.savings_type, obj.amount)


class SavingsDepositAdmin(admin.ModelAdmin):
    list_display = ('member', 'savings_type', 'amount', 'date')

    def save_model(self, request, obj, form, change):
        SavingsDeposit.deposit_savings(obj.member, obj.savings_type, obj.amount)


from savings.models import Savings, SavingsType, SavingsWithdrawal, SavingsDeposit


class SavingAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'savings_type', 'amount', 'date')
    list_filter = ['savings_type', 'date', 'amount']
    search_fields = []


class SavingsTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'compulsory', 'interval', 'minimum_amount', 'maximum_amount', 'interest_rate')
    list_filter = ['name']
    search_fields = ['name', 'category']


admin.site.register(Savings, SavingsAdmin)
admin.site.register(SavingsType, SavingsTypeAdmin)
admin.site.register(SavingsWithdrawal, SavingsWithdrawalAdmin)
admin.site.register(SavingsDeposit, SavingsDepositAdmin)
