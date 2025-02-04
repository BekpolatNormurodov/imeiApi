from django.urls import path
from rest_framework import routers
from api.views import CustomUserViewSet, ArizaViewSet, JinoyatIshiViewSet, ProfileViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
router = routers.SimpleRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('profile', ProfileViewSet, basename='profile')
router.register('ariza', ArizaViewSet, basename='ariza')
router.register('jinoyatishi', JinoyatIshiViewSet, basename='jinoyatishi')
urlpatterns += router.urls
