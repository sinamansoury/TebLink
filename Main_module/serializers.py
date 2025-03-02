from rest_framework import serializers
from .models import  Speciality


class ConsultantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Speciality
        fields = '__all__'