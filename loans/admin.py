# Register your models here.
from django.contrib import admin
from django.template.defaultfilters import title
from django.utils.safestring import mark_safe
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from loans.models import SecuritySavings, LoanRuleShares, LoanRuleSavings, LoanRuleOther, SecurityGuarantor
from loans.models import LoanType, LoanApplication, SecurityArticle, Loan, Security, SecurityShares


class LoanAdmin(admin.ModelAdmin):
    list_display = ('member', 'application', 'approval_date', 'amount', 'payment_period', 'loan_type')
    list_filter = ['approval_date', 'payment_period', 'loan_type']
    search_fields = ['loan_type', 'member']


class LoanRuleSharesAdmin(admin.TabularInline):
    model = LoanRuleShares
    extra = 0


class LoanRuleSavingsAdmin(admin.TabularInline):
    model = LoanRuleSavings
    extra = 0


class LoanRuleOtherAdmin(admin.TabularInline):
    model = LoanRuleOther
    extra = 0


class LoanTypeAdmin(admin.ModelAdmin):
    inlines = (LoanRuleSharesAdmin, LoanRuleSavingsAdmin, LoanRuleOtherAdmin)


class SecurityChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Security


class SecurityArticleAdmin(SecurityChildAdmin):
    list_display = ('__unicode__',)


class SecuritySharesAdmin(SecurityChildAdmin):
    list_display = ('__unicode__',)


class SecuritySavingsAdmin(SecurityChildAdmin):
    list_display = ('__unicode__',)


class SecurityGuarantorAdmin(SecurityChildAdmin):
    list_display = ('__unicode__',)


class SecurityAdmin(PolymorphicParentModelAdmin):
    base_model = Security
    child_models = (
        (SecuritySavings, SecuritySavingsAdmin),
        (SecurityShares, SecuritySharesAdmin),
        (SecurityArticle, SecurityArticleAdmin),
        (SecurityGuarantor, SecurityGuarantorAdmin),
    )

    polymorphic_list = True
    list_display = ('__unicode__',)


class SecuritySavingsInline(admin.TabularInline):
    model = SecuritySavings
    extra = 0
    exclude = ('loan',)
    readonly_fields = ('value',)


class SecuritySharesInline(admin.TabularInline):
    model = SecurityShares
    extra = 0
    exclude = ('loan',)
    readonly_fields = ('value',)


class SecurityArticleInline(admin.TabularInline):
    model = SecurityArticle
    extra = 0
    exclude = ('loan',)
    readonly_fields = ('value',)


class SecurityGuarantorInline(admin.TabularInline):
    model = SecurityGuarantor
    extra = 0
    exclude = ('loan',)
    readonly_fields = ('value',)


class LoanApplicationAdmin(admin.ModelAdmin):
    fields = ('status', 'application_number', 'member', 'amount', 'purpose', 'payment_period', 'loan_type',
              'security_details', 'security_satisfied', 'comment',)
    list_display = (
    'member','application_number', 'security_satisfied',  'application_date', 'amount', 'loan_type', 'status', 'comment',)
    ordering = ('-application_date',)
    readonly_fields = ('application_number', 'member', 'amount', 'purpose', 'payment_period', 'loan_type',
                       'security_details', 'security_satisfied',)
    list_filter = ('application_date', 'payment_period',)
    search_fields = ('member',)
    inlines = (SecuritySharesInline, SecuritySavingsInline, SecurityArticleInline, SecurityGuarantorInline)

    def save_model(self, request, obj, form, change):
        old = LoanApplication.objects.get(pk=obj.pk)
        if form.changed_data and obj.status != old.status:
            if obj.status == 'approved':
                if obj.approve_loan_application(request.user):
                    self.message_user(request, "Loan successfully approved.")
                else:
                    self.message_user(request, "Loan failed to be approved.")
            elif obj.status == 'rejected':
                obj.reject_loan_application(request.user)


admin.site.register(Loan, LoanAdmin)
admin.site.register(LoanType, LoanTypeAdmin)
admin.site.register(LoanApplication, LoanApplicationAdmin)
admin.site.register(SecurityArticle, SecurityArticleAdmin)
admin.site.register(Security, SecurityAdmin)
admin.site.register(SecurityShares, SecuritySharesAdmin)
admin.site.register(SecuritySavings, SecuritySavingsAdmin)
admin.site.register(SecurityGuarantor, SecurityGuarantorAdmin)
