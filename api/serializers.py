from rest_framework import serializers
from api.models import *

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'imei','namber','model', 'color', 'info')
        