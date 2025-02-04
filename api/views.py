from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from api.serializers import CustomUserSerializer, ArizaModelSerializer, JinoyatIshiSerializer, ProfileSerializer
from api.permissions import IsSuperUser, IsOwnerOrReadOnly, IsJtonOwner
from api.models import CustomUser, ArizaModel, JinoyatIshiModel
from api.paginations import CustomPagination


class CustomUserViewSet(ModelViewSet):
    permission_classes = [IsJtonOwner | IsSuperUser, ]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, ]
    filterset_fields = ['is_active', 'bolim__name', 'boshqarma__name', 'unvon__name']
    search_fields = ['username', 'first_name', 'last_name', 'unvon__name', str('phone_number'), 'bolim__name',
                     'boshqarma__name', ]
    ordering_fields = ['bolim__name', 'boshqarma__name', 'created_at', 'updated_at', 'unvon__name']


class ArizaViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsAuthenticated, IsOwnerOrReadOnly, ]
    queryset = ArizaModel.objects.all()
    serializer_class = ArizaModelSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['is_deleted', 'status', 'color', 'model']
    search_fields = ['owner__first_name', 'owner__last_name', 'owner__father_name', str('owner__phone_number'),
                     'owner__jshir',
                     'imei', 'model', 'color', ]
    ordering_fields = ['status', 'created_at', 'updated_at', 'model', 'imei', 'color', ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(author=self.request.user, is_deleted=False)


class JinoyatIshiViewSet(ModelViewSet):
    permission_classes = [IsSuperUser | IsOwnerOrReadOnly, IsAuthenticated, ]
    queryset = JinoyatIshiModel.objects.all()
    serializer_class = JinoyatIshiSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['is_deleted', 'status']
    search_fields = ['fish', 'jshir', 'phone_number', ]
    ordering_fields = ['status', 'created_at', 'updated_at', 'fish']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(author=self.request.user, is_deleted=False)

    def get_search_fields(self, view, request):
        if request.data.search_fields:
            return request.data.search_fields
        return ['fish', 'jshir', 'phone_number', ]


class ProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsJtonOwner, ]
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)
