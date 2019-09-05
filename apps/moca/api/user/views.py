from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed, AuthenticationFailed
from rest_framework.views import (APIView)
from rest_framework.generics import (GenericAPIView)
from .serializers import AddressSerializer, FCMDeviceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from moca.models import User
from .serializers import UserSerializer, UserSerializerForUpdate
from knox.models import AuthToken


class UserAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

    # @permission_classes([IsAuthenticated])
    def put(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        if user_id is not None:
            raise MethodNotAllowed
        elif user_id != request.user:
            raise AuthenticationFailed('UserId in URL doesnt match with the id of authenticated user')

        saved_addresses = []
        saved_devices = []
        for device in request.data['fcmdevices']:
            device_serializer = FCMDeviceSerializer(data=device)
            device_serializer.is_valid(raise_exception=True)
            saved_device = device_serializer.save()
            saved_devices.append(saved_device)

        for address in request.data['addresses']:
            try:
                address.user = request.user.id
            except AttributeError:
                address["user"] = request.user.id
            address_serializer = AddressSerializer(data=address)
            address_serializer.is_valid(raise_exception=True)
            saved_address = address_serializer.save()
            saved_addresses.append(saved_address)

        latest_user = User.objects.filter(id=request.user.id)
        print('This is latest user' + latest_user)
        return Response({
            "user": UserSerializerForUpdate(latest_user, context=self.get_serializer_context()).data
        })
