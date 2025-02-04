from django.db import models
from django.contrib.auth.models import AbstractUser

from api.middleware import get_current_user

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

    # def delete(self, *args, **kwargs):
    #     """Override the delete method to implement soft delete."""
    #     user = get_current_user()  # Get the user from thread-local storage
    #     print(user)
    #     if self.is_deleted:
    #         if user and user.is_superuser:
    #             super(BaseModel, self).delete(*args, **kwargs)  # Perform real delete
    #         else:
    #             return  # Do nothing if the user is not authorized to delete it permanently
    #     else:
    #         self.is_deleted = True
    #         self.save()

    def soft_delete(self, *args, **kwargs):
        """Restore a soft-deleted instance."""
        if self.is_deleted:
            self.is_deleted = False
        else:
            self.is_deleted = False
        self.save()


class Boshqarma(BaseModel, models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Bolim(BaseModel, models.Model):
    name = models.CharField(max_length=255)
    bolim = models.ForeignKey(Boshqarma, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Unvon(BaseModel, models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class CustomUser(BaseModel, AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    boshqarma = models.ForeignKey(Boshqarma, on_delete=models.SET_NULL, null=True)
    bolim = models.ForeignKey(Bolim, on_delete=models.SET_NULL, null=True)
    unvon = models.ForeignKey(Unvon, on_delete=models.SET_NULL, null=True)
    father_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=13, unique=True)
    jton = models.CharField(max_length=8, unique=True)
    ishjoylari = models.ManyToManyField(Boshqarma, related_name='ishjoylari', blank=True)

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"


class ClientData(BaseModel, models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=13)
    jshir = models.CharField(max_length=14)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.father_name}"

    # def delete(self, *args, **kwargs):
    #     if self.is_deleted:
    #         self.is_deleted = False
    #     else:
    #         self.is_deleted = True
    #     self.save()
    #     return self


class ArizaModel(BaseModel, models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    owner = models.ForeignKey(ClientData, on_delete=models.CASCADE)
    imei = models.CharField(max_length=255)
    last_simcard = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    info = models.TextField()
    shakl1 = models.CharField(max_length=30)
    status = models.CharField(
        max_length=50,
        choices=STATUS_ARIZA,
        default='yaratildi',
    )

    def __str__(self):
        return f"{self.owner} {self.imei} {self.model}"

    def delete(self, *args, **kwargs):
        self.owner.delete()
    #     if self.is_deleted:
    #         self.is_deleted = False
    #     else:
    #         self.is_deleted = True
    #     self.save()
    #     return self


class JinoyatIshiModel(BaseModel, models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    jinoyat_raqami = models.CharField(max_length=255)
    fish = models.CharField(max_length=255)
    jshir = models.CharField(max_length=255)
    info = models.TextField()
    phone_number = models.CharField(max_length=13)
    status = models.CharField(
        max_length=50,
        choices=STATUS_JINOYAT,
        default='yopilgan',
    )

    def __str__(self):
        return self.fish
