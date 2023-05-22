from django.conf.urls import patterns, include, url
from django.contrib import admin

from members import views
from shares import views as shares_views
from savings import views as savings_views
from loans import views as loan_views

urlpatterns = patterns('',
                       url(r'^$', views.MemberList.as_view()),
                       url(r'^(?P<pk>[0-9]+)/$', views.MemberDetail.as_view()),
                       url(r'^(?P<pk>[0-9]+)/shares$', shares_views.SharesView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/shares/purchases$', shares_views.SharePurchasesView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/shares/transfers$', shares_views.ShareTransfersView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/shares/transactions$', shares_views.ShareTransactionsView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/savings$', savings_views.SavingsView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/savings/deposits$', savings_views.SavingsDepositView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/savings/withdrawals$', savings_views.SavingsWithdrawalView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/savings/transactions$', savings_views.SavingsTransactionsView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/loans$', loan_views.LoansView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/loans/applications$', loan_views.LoanApplicationView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/loans/securities$', loan_views.SecurityView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/loans/securities/shares$', loan_views.LoanSecuritySharesView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/loans/securities/savings$', loan_views.LoanSecuritySavingsView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/loans/securities/articles$', loan_views.LoanSecurityArticlesView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/loans/securities/guarantors$', loan_views.LoanSecurityGuarantorsView.as_view()),
                       url(r'^(?P<pk>[0-9]+)/notifications', views.NotificationView.as_view()),
                       )