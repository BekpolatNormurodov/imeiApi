from rest_framework.generics import *
from api.models import *
from .serializers import *
# from rest_framework import permissions

# Device Api
class DeviceApiView(ListAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceApiCreate(ListCreateAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceApiUpdate(RetrieveUpdateDestroyAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer