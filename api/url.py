from django.urls import path
from .views import *

urlpatterns = [
    # Device urls
    path('device/',DeviceApiView.as_view()),
    path('device/create/',DeviceApiCreate.as_view()),
    path('device/<int:pk>',DeviceApiUpdate.as_view()),
]