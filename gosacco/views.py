from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from gosacco.account_utils import decode_data, register_user, create_registration_link
from gosacco.serializers import UserRegistrationSerializer


class AccountView(APIView):
    permission_classes = ()

    def post(self, request, format=None):
        """
        Register New User
        """
        hash = request.query_params.get('h', None)
        info = request.query_params.get('d', None)
        check = decode_data(hash, info)
        now_utc = datetime.utcnow()
        expire_utc = datetime.utcfromtimestamp(check['expire'])
        print(now_utc, expire_utc)

        if isinstance(check, Exception):
            print(check.message.__str__())
            return Response(status=status.HTTP_403_FORBIDDEN)
        if now_utc < expire_utc:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = register_user(username=serializer.validated_data['username'],
                                    password=serializer.validated_data['password'],
                                    email=serializer.validated_data['email'],
                                    first_name=serializer.validated_data['first_name'],
                                    last_name=serializer.validated_data['last_name'],)
                link = create_registration_link(user)
                if link:
                    return Response({"link": link}, status=status.HTTP_201_CREATED)

                return Response({"detail": "User already Exists"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Link expired. Request another."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)
