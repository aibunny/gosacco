from django.contrib.auth.models import User
from notifications.models import Notification
from rest_framework import serializers, viewsets

from members.models import Member, Group, NextOfKin


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'email')


class MemberSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Member

        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'monthly_income', 'occupation', 'bank', 'account_number', 'signature',
                  'id_type', 'id_number', 'address', 'city', 'nationality','comments')

    def get_username(self,obj):
        return obj.user.username

    def get_first_name(self,obj):
        return obj.user.first_name

    def get_last_name(self,obj):
        return obj.user.last_name

    def get_email(self,obj):
        return obj.user.email


class MemberPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('user', 'phone_number', 'monthly_income', 'occupation', 'bank', 'account_number', 'signature',
                  'id_type', 'id_number', 'address', 'city', 'nationality','comments')


class MemberUserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    def get_username(self,obj):
        return obj.user.username

    def get_first_name(self,obj):
        return obj.user.first_name

    def get_last_name(self,obj):
        return obj.user.last_name

    class Meta:
        model = Member
        depth = 0
        fields = ('id', 'username', 'first_name', 'last_name')





class GroupSerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(many=True)
    leader = serializers.StringRelatedField()

    class Meta:
        model = Group


class GroupMemberSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        # fields = ()


class NextOfKinSerializer(serializers.ModelSerializer):

    class Meta:
        model = NextOfKin


class MemberViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        """
        Return a list of objects.

        """
        return super(MemberViewSet, self).list(request, *args, **kwargs)


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    verb = serializers.StringRelatedField()
    target = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ('actor', 'verb', 'target', 'timesince', 'description', 'unread')