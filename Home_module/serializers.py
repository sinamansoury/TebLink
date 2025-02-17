from rest_framework import serializers
from Home_module.models import Doctors, AppointmentSlot


class DoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        fields = '__all__'

class AppointmentSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentSlot
        fields = ['id', 'doctor', 'time_slot', 'time', 'status']
