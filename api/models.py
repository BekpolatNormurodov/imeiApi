from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

STATUS_ARIZA = [
    ('yaratildi', "Yaratildi"),
    ('qidiruvda', "Qidiruvda"),
    ('topild', 'Topildi'),
    ('yopildi', 'Yakunlandi'),
]
STATUS_JINOYAT = [
    ('ochilgan', "Yangi"),
    ('qaytarilgan', "Qaytarilgan"),
    ('sud', "Sudga chiqarildi"),
    ('yopildi', 'Yopilgan'),
]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def soft_delete(self, *args, **kwargs):
        """Toggle soft delete status."""
        self.is_deleted = not self.is_deleted
        self.save()


class Boshqarma(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Bolim(BaseModel):
    name = models.CharField(max_length=255)
    boshqarma = models.ForeignKey(Boshqarma, on_delete=models.CASCADE, related_name='bolimlar')

    def __str__(self):
        return self.name


class Unvon(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser, BaseModel):
    phone_validator = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak"
    )
    jton_validator = RegexValidator(
        regex=r'^\d{8}$',
        message="JTON 8 ta raqamdan iborat bo'lishi kerak"
    )
    
    username = models.CharField(max_length=255, unique=True, db_index=True)
    boshqarma = models.ForeignKey(Boshqarma, on_delete=models.SET_NULL, null=True, blank=True)
    bolim = models.ForeignKey(Bolim, on_delete=models.SET_NULL, null=True, blank=True)
    unvon = models.ForeignKey(Unvon, on_delete=models.SET_NULL, null=True, blank=True)
    father_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=13, unique=True, db_index=True, validators=[phone_validator])
    jton = models.CharField(max_length=8, unique=True, db_index=True, validators=[jton_validator])
    lavozimi = models.CharField(max_length=250, blank=True, null=True)
    ishjoylari = models.ManyToManyField(Boshqarma, related_name='ishjoylari', blank=True)

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"


class ClientData(BaseModel):
    phone_validator = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak"
    )
    jshir_validator = RegexValidator(
        regex=r'^\d{14}$',
        message="JSHIR 14 ta raqamdan iborat bo'lishi kerak"
    )
    
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=13, validators=[phone_validator])
    jshir = models.CharField(max_length=14, validators=[jshir_validator], db_index=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.father_name}"


class ArizaModel(BaseModel):
    imeiApi_validator = RegexValidator(
        regex=r'^\d{15}$',
        message="imeiApi 15 ta raqamdan iborat bo'lishi kerak"
    )
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    owner = models.ForeignKey(ClientData, on_delete=models.CASCADE)
    imeiApi = models.CharField(max_length=15, validators=[imeiApi_validator], db_index=True)
    last_simcard = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255)
    color = models.CharField(max_length=255, blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    shakl1 = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_ARIZA,
        default='yaratildi',
    )

    def __str__(self):
        return f"{self.owner} {self.imeiApi} {self.model}"


class JinoyatIshiModel(BaseModel):
    phone_validator = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak"
    )
    jshir_validator = RegexValidator(
        regex=r'^\d{14}$',
        message="JSHIR 14 ta raqamdan iborat bo'lishi kerak"
    )
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    jinoyat_raqami = models.CharField(max_length=255, db_index=True)
    fish = models.CharField(max_length=255)
    jshir = models.CharField(max_length=14, validators=[jshir_validator], db_index=True)
    info = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=13, validators=[phone_validator])
    status = models.CharField(
        max_length=50,
        choices=STATUS_JINOYAT,
        default='ochilgan',
    )

    def __str__(self):
        return self.fish


class XisobgaQoyishSababi(BaseModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sabab_name = models.CharField(max_length=255)

    def __str__(self):
        return self.sabab_name


class XisobTuri(BaseModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tur_nomi = models.CharField(max_length=255)

    def __str__(self):
        return self.tur_nomi


class GuruhgaOid(BaseModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=255)

    def __str__(self):
        return self.device_type


class Nomlanishi(BaseModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    namen = models.CharField(max_length=255)

    def __str__(self):
        return self.namen


class Rusumi(BaseModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class LostDeviceModel(BaseModel):
    imeiApi_validator = RegexValidator(
        regex=r'^\d{15}$',
        message="imeiApi 15 ta raqamdan iborat bo'lishi kerak"
    )
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    imeiApi = models.CharField(max_length=15, blank=True, null=True, validators=[imeiApi_validator], db_index=True)
    last_simcard = models.CharField(max_length=255, blank=True, null=True)
    gruhga_oid = models.ForeignKey(GuruhgaOid, on_delete=models.SET_NULL, null=True)
    nomlanishi = models.ForeignKey(Nomlanishi, on_delete=models.SET_NULL, null=True)
    soni = models.CharField(max_length=255, blank=True, null=True)
    rusumi = models.ForeignKey(Rusumi, on_delete=models.SET_NULL, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    zavod = models.CharField(max_length=255, blank=True, null=True)
    rangi = models.CharField(max_length=255, blank=True, null=True)
    tegishlilik = models.CharField(max_length=255, blank=True, null=True)
    xususiyatlari = models.TextField(blank=True, null=True)
    ishlab_chiqarilgan_yili = models.PositiveIntegerField(blank=True, null=True)
    device_rasmmi = models.ImageField(upload_to="device_rasmmi", blank=True, null=True)
    sababi = models.ForeignKey(XisobgaQoyishSababi, on_delete=models.SET_NULL, null=True)
    xisob_turi = models.ForeignKey(XisobTuri, on_delete=models.SET_NULL, null=True)
    xujat_raqami = models.CharField(max_length=255, blank=True, null=True)
    xujat_yaratilgan_sana = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    tashkilot = models.CharField(max_length=255, blank=True, null=True)
    xudud = models.CharField(max_length=255, blank=True, null=True)
    organ = models.CharField(max_length=255, blank=True, null=True)
    modda = models.CharField(max_length=255, blank=True, null=True)
    qism = models.CharField(max_length=255, blank=True, null=True)
    band = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.imeiApi} {self.model}"

