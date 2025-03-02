from rest_framework import serializers
from Home_module.models import Doctors, Degree, Specialty


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, min_length=11)

    def validate_phone(self, value):
        if not value.isdigit() or not value.startswith('0'):
            raise serializers.ValidationError("شماره تلفن باید 11 رقم و با 0 شروع شود.")
        return value

class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = '__all__'

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'

class DoctorRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctors
        fields = ['phone', 'name', 'last_name', 'id_code', 'birthday', 'number', 'sex', 'degree', 'degree_name', 'speciality_name']


