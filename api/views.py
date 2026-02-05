from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from api.serializers import CustomUserSerializer, ArizaModelSerializer, JinoyatIshiSerializer, ProfileSerializer, \
    LostDeviceSerializer
from api.permissions import IsSuperUser, IsOwnerOrReadOnly, IsJtonOwner
from api.models import CustomUser, ArizaModel, JinoyatIshiModel, LostDeviceModel
from api.paginations import CustomPagination

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import pandas as pd
from io import BytesIO

class CustomUserViewSet(ModelViewSet):
    permission_classes = [IsJtonOwner | IsSuperUser, ]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, ]
    filterset_fields = ['is_active', 'bolim__name', 'boshqarma__name', 'unvon__name']
    search_fields = ['username', 'first_name', 'last_name', 'unvon__name', 'phone_number', 'bolim__name',
                     'boshqarma__name', ]
    ordering_fields = ['bolim__name', 'boshqarma__name', 'created_at', 'updated_at', 'unvon__name']


class ArizaViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, (IsSuperUser | IsOwnerOrReadOnly)]
    queryset = ArizaModel.objects.all()
    serializer_class = ArizaModelSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['is_deleted', 'status', 'color', 'model']
    search_fields = ['owner__first_name', 'owner__last_name', 'owner__father_name', 'owner__phone_number',
                     'owner__jshir',
                     'imeiApi', 'model', 'color', ]
    ordering_fields = ['status', 'created_at', 'updated_at', 'model', 'imeiApi', 'color', ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(author=self.request.user, is_deleted=False)


class JinoyatIshiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, (IsSuperUser | IsOwnerOrReadOnly)]
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


class ProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsJtonOwner, ]
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)


class LostDeviceRegisterViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = LostDeviceModel.objects.all()
    serializer_class = LostDeviceSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['is_deleted', 'author']
    search_fields = ['imeiApi', 'serial_number', 'last_simcard', ]
    ordering_fields = ['zavod', 'created_at', 'updated_at', 'model']
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(author=self.request.user, is_deleted=False)


class ExcelUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        if 'file' not in request.data:
            return Response({"error": "Fayl yuklanmadi"}, status=status.HTTP_400_BAD_REQUEST)

        excel_file = request.FILES['file']
        try:
            # Excel faylini pandas yordamida o‘qish
            df = pd.read_excel(excel_file, engine='openpyxl')
            data = df.to_dict(orient='records')  # Ma’lumotlarni JSON formatiga o‘tkazish
            return Response({"data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ExportExcelView(APIView):
    def get(self, request, format=None):
        # Ma’lumotlarni tayyorlash (masalan, modeldan olish)
        data = [
            {"id": 1, "name": "Ali", "age": 25},
            {"id": 2, "name": "Vali", "age": 30},
        ]

        # Pandas DataFrame ga aylantirish
        df = pd.DataFrame(data)

        # Excel faylini yaratish
        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)

        # HttpResponse orqali faylni qaytarish
        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'
        return response
