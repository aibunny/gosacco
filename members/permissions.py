from rest_framework import permissions
from members.models import Member
from shares.models import ShareTransfer


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow members to access it.
    """
    message = "You aren't allowed to access this."

    def has_object_permission(self, request, view, obj):

        # Members can
        if request.method in ("GET", "POST", "HEAD",):
            if isinstance(obj, Member):
                return (obj == request.user.member) or request.user.is_staff
            else:
                return (obj.member == request.user.member) or request.user.is_staff
        elif request.method in ("DELETE", "PUT",):
            return request.user.is_staff
