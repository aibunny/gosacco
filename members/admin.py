from members.models import Member, Group, NextOfKin

__author__ = 'mark'
from django.contrib import admin


class MemberAdmin(admin.ModelAdmin):
    pass


class GroupAdmin(admin.ModelAdmin):
    pass


class NextOfKinAdmin(admin.ModelAdmin):
    pass


admin.site.register(Member, MemberAdmin)
admin.site.register(NextOfKin, NextOfKinAdmin)
admin.site.register(Group, GroupAdmin)
