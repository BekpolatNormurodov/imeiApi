from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import Boshqarma, CustomUser, Unvon, Bolim, ClientData, ArizaModel, \
    JinoyatIshiModel, LostDeviceModel, Rusumi, XisobTuri, GuruhgaOid, Nomlanishi, XisobgaQoyishSababi


class BoshqarmaAdmin(admin.ModelAdmin):
    model = Boshqarma
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


class CustomUserAdmin(UserAdmin):  # Correct inheritance
    model = CustomUser
    list_display = ('id', 'phone_number', 'jton', 'first_name', 'last_name', 'father_name', 'lavozimi')
    list_display_links = ('id', 'phone_number')
    search_fields = ('phone_number', 'jton', 'first_name', 'last_name', 'lavozimi')
    list_filter = ('ishjoylari',)
    fieldsets = (
        ("Auth Info", {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'father_name', 'phone_number', 'jton')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Work Info', {'fields': ('boshqarma', 'bolim', 'unvon', 'lavozimi', 'ishjoylari')}),
    )


class ClientDataAdmin(admin.ModelAdmin):
    model = ClientData
    list_display = ('id', 'first_name', 'last_name', 'father_name', 'phone_number', 'jshir', 'is_deleted')
    list_display_links = ('id', 'phone_number')
    search_fields = ('phone_number', 'jshir', 'first_name', 'last_name')
    list_filter = ('phone_number',)
    fieldsets = (
        ('Client Info', {'fields': ('first_name', 'last_name', 'father_name', 'phone_number', 'jshir')}),
        ('Change Info', {'fields': ('is_deleted',)}),
    )


class UnvonAdmin(admin.ModelAdmin):
    model = Unvon
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


class BolimAdmin(admin.ModelAdmin):
    model = Bolim
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


class ArizaModelAdmin(admin.ModelAdmin):
    model = ArizaModel
    list_display = (
        'id', 'author', 'owner', 'status', 'imeiApi', 'last_simcard', 'model', 'color', 'created_at', 'updated_at',
        'is_deleted')
    list_display_links = ('id', 'imeiApi')
    list_filter = ('status', 'model', 'color', 'is_deleted')
    search_fields = ('imeiApi', 'model', 'color')
    fieldsets = (
        ('Ariza Info', {'fields': ('author', 'status', 'imeiApi', 'last_simcard', 'model', 'color')}),
        ('Owner Info', {'fields': ('owner',)}),
        ('Change Info', {'fields': ('is_deleted',)}),
    )


class JinoyatIshiModelAdmin(admin.ModelAdmin):
    model = JinoyatIshiModel
    list_display = ('id', 'author', 'fish', 'jshir', 'jinoyat_raqami',)
    list_display_links = ('id', 'fish', 'jshir',)
    search_fields = ('fish', 'jshir', 'jinoyat_raqami',)
    list_filter = ('status',)
    fieldsets = (
        ('Ariza Info', {'fields': ('author', 'fish', 'jshir', 'info', 'phone_number',)}),
        ('Change Info', {'fields': ('is_deleted', 'status',)}),
    )


admin.site.register(Boshqarma, BoshqarmaAdmin)
admin.site.register(Bolim, BolimAdmin)
admin.site.register(Unvon, UnvonAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ClientData, ClientDataAdmin)
admin.site.register(ArizaModel, ArizaModelAdmin)
admin.site.register(JinoyatIshiModel, JinoyatIshiModelAdmin)
admin.site.register(LostDeviceModel)
admin.site.register(Rusumi)
admin.site.register(XisobTuri)
admin.site.register(GuruhgaOid)
admin.site.register(Nomlanishi)
admin.site.register(XisobgaQoyishSababi)
