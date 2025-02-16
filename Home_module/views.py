from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from Home_module.models import Doctors, TimeSlot, AppointmentSlot
from Home_module.serializers import DoctorsSerializer, AppointmentSlotSerializer


# Create your views here.

class DoctorsView(TemplateView):
    template_name = 'بشنث.html'

class DoctorsApiView(APIView):
    def get(self, request, consultant):
        if not consultant:
            return Response({'error': 'تخصص موجود نیست'}, status=status.HTTP_400_BAD_REQUEST)

        doctors = Doctors.objects.filter(consultant__consultant=consultant)

        if not doctors.exists():
            return Response({'error': 'پزشکان با این تخصص یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorsSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DayApiView(APIView):
    def get(self, request):
        doctor_id = request.GET.get("doctor_id")

        if not doctor_id:
            return Response({'error': 'دکتر وجود ندارئ'},status=status.HTTP_400_BAD_REQUEST)

        doctor = get_object_or_404(Doctors, id=doctor_id)
        slots = TimeSlot.objects.filter(doctor=doctor).values_list('days__name', flat=True).distinct()

        if not slots:
            return Response({'error':'روز پیدا نشد'},status=status.HTTP_400_BAD_REQUEST)

        return Response(list(slots), status=status.HTTP_200_OK)

class AppointmentApiView(APIView):
    def get(self, request):
        doctor_id = request.GET.get("doctor_id")
        day = request.GET.get("days")

        if not doctor_id:
            return Response({'error': 'دکتر پیدا نشد'}, status=status.HTTP_400_BAD_REQUEST)

        if not day:
            return Response({'error': 'روز پیدا نشد'}, status=status.HTTP_400_BAD_REQUEST)

        doctor = get_object_or_404(Doctors, id=doctor_id)

        slots = TimeSlot.objects.filter(doctor=doctor, days__name=day)

        if not slots.exists():
            return Response({'error': 'بازه زمانی برای این روز وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)

        appointments = AppointmentSlot.objects.filter(time_slot__in=slots, doctor=doctor, status='empty')

        if not appointments.exists():
            return Response({'error': 'هیچ نوبت خالی برای این روز وجود ندارد'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AppointmentSlotSerializer(appointments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)