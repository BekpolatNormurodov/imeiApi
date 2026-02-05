from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import CustomUser, Bolim, Boshqarma, Unvon, ArizaModel, ClientData, JinoyatIshiModel, LostDeviceModel


class BoshqarmaSerializer(ModelSerializer):
    class Meta:
        model = Boshqarma
        fields = ['id', 'name']


class BolimSerializer(ModelSerializer):
    class Meta:
        model = Bolim
        fields = ['id', 'name']


class UnvonSerializer(ModelSerializer):
    class Meta:
        model = Unvon
        fields = ['id', 'name']


class ProfileSerializer(ModelSerializer):
    ishjoylari = BoshqarmaSerializer(many=True, read_only=True)
    bolim = BolimSerializer(read_only=True)
    boshqarma = BoshqarmaSerializer(many=False, read_only=True)
    unvon = UnvonSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'jton', 'first_name', 'last_name', 'father_name', 'lavozimi',
                  'boshqarma',
                  'bolim',
                  'unvon',
                  'ishjoylari']
        depth = 1


class CustomUserSerializer(ModelSerializer):
    ishjoylari = BoshqarmaSerializer(many=True, read_only=True)
    bolim = BolimSerializer(read_only=True)
    boshqarma = BoshqarmaSerializer(many=False, read_only=True)
    unvon = UnvonSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'jton', 'first_name', 'last_name', 'father_name',
                  'boshqarma',
                  'bolim',
                  'unvon',
                  'lavozimi',
                  'ishjoylari']
        depth = 1

    def create(self, validated_data):
        username = validated_data['phone_number']
        password = validated_data['jton']
        ishjoylari_data = validated_data.pop('ishjoylari', None)
        # Foydalanuvchi obyektini yaratamiz
        user = CustomUser.objects.create(**validated_data)
        user.username = username
        # user.is_active = False
        user.set_password(password)  # Parolni xesh qilish
        user.save()
        # Many-to-Many maydonni sozlaymiz (agar u mavjud bo'lsa)
        if ishjoylari_data:
            user.ishjoylari.set(ishjoylari_data)

        # Foydalanuvchini qaytaramiz
        return user

    def update(self, instance, validated_data):
        # Validated_data dagi barcha maydonlarni yangilash
        for field, value in validated_data.items():
            if field == 'ishjoylari':  # Many-to-Many maydonlar uchun maxsus ishlov
                instance.ishjoylari.set(value)
            elif field == 'jton':  # Parolni sozlash uchun maxsus ishlov
                instance.set_password(value)
            else:
                setattr(instance, field, value)  # Fieldni dinamik ravishda yangilash

        # O'zgarishlarni saqlash
        instance.save()
        return instance


class ArizaOwnerSerializer(ModelSerializer):
    class Meta:
        model = ClientData
        fields = ['id', 'first_name', 'last_name', 'father_name', 'phone_number', 'jshir']


class ArizachiSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class ArizaModelSerializer(ModelSerializer):
    owner = ArizaOwnerSerializer(read_only=True)
    author = ArizachiSerializer(read_only=True)

    jshir = serializers.CharField(write_only=True, required=True)  # New field for jshir
    phone_number = serializers.CharField(write_only=True, required=True)  # New field for phone number
    fish = serializers.CharField(write_only=True, required=True)  # New field for full name

    class Meta:
        model = ArizaModel
        fields = [
            'id', 'author', 'status', 'imeiApi', 'last_simcard', 'model', 'color', 'info', 'shakl1', 'created_at', 'updated_at', 'is_deleted',
            'owner', 'jshir', 'phone_number', 'fish',  # Added new fields
        ]

    def create(self, validated_data):
        # Extract client-related data from validated_data
        fish = validated_data.pop('fish').split()
        clientdata = {
            'jshir': validated_data.pop('jshir'),
            'phone_number': validated_data.pop('phone_number'),
            'first_name': (fish[1]) if len(fish) > 1 else None,
            'last_name': fish[0],
            'father_name': " ".join(fish[2:]) if len(fish) > 2 else None,
        }

        # Create the owner (ClientData)
        owner = ClientData.objects.create(**clientdata)

        # Associate owner with ArizaModel and create the record
        validated_data['owner'] = owner
        validated_data['author'] = self.context['request'].user  # Add the author (current user)
        ariza = ArizaModel.objects.create(**validated_data)
        return ariza

    def update(self, instance, validated_data):
        # Extract and process owner-related fields
        owner_fields = ['first_name', 'last_name', 'father_name', 'phone_number', 'jshir']
        if 'fish' in validated_data and validated_data['fish']:
            fish = validated_data.pop('fish').split()
            validated_data['first_name'] = (fish[1]) if len(fish) > 1 else None
            validated_data['last_name'] = fish[0]
            validated_data['father_name'] = " ".join(fish[2:]) if len(fish) > 2 else None
        owner_data = {field: validated_data.pop(field, None) for field in owner_fields if field in validated_data}
        # Update owner if data is provided
        if owner_data:
            for field, value in owner_data.items():
                if value is not None:  # Avoid overwriting with None
                    setattr(instance.owner, field, value)
            instance.owner.save()

        # Qolgan maydonlarni yangilash
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        return instance


class JinoyatIshiSerializer(ModelSerializer):
    author = ArizachiSerializer(read_only=True)

    class Meta:
        model = JinoyatIshiModel
        fields = ['id', 'author', 'jinoyat_raqami', 'fish', 'jshir', 'info', 'phone_number', 'status', 'created_at', 'updated_at', 'is_deleted']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        jinoyat = JinoyatIshiModel.objects.create(**validated_data)
        return jinoyat


class LostDeviceSerializer(ModelSerializer):
    author = ArizachiSerializer(read_only=True)

    class Meta:
        model = LostDeviceModel
        fields = [
            'id', 'serial_number', 'imeiApi', 'last_simcard', 'soni', 'model', 'zavod', 'rangi', 'tegishlilik', 'xususiyatlari',
            'ishlab_chiqarilgan_yili', 'device_rasmmi', 'xujat_raqami', 'tashkilot', 'xudud', 'organ', 'modda', 'qism',
            'band', 'gruhga_oid', 'nomlanishi', 'rusumi', 'sababi', 'xisob_turi', 'author', 'created_at', 'updated_at', 'is_deleted'
        ]
        depth = 1

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        lostdevice = LostDeviceModel.objects.create(**validated_data)
        return lostdevice
