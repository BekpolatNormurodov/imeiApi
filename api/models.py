from django.db import models

class Device(models.Model):
    imei = models.CharField(max_length=15, null=True)
    namber = models.CharField(max_length=13, null=True)
    model = models.CharField(max_length=200, null=True)
    color = models.CharField(max_length=200, null=True)
    info = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.imei[:15]