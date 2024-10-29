from django.urls import path
from .views import *

urlpatterns = [
    # Device urls
    path('',DeviceApiView.as_view()),
    path('create/',DeviceApiCreate.as_view()),
    path('<int:pk>',DeviceApiUpdate.as_view()),
]