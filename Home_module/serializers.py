from rest_framework import serializers
from Home_module.models import Doctors, AppointmentSlot, Services


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['name', 'min_price', 'max_price']

class DoctorsSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True)

    class Meta:
        model = Doctors
        fields = '__all__'

class AppointmentSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentSlot
        fields = ['id', 'doctor', 'time_slot', 'time', 'status']
