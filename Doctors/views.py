import random
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from Doctors.serializers import PhoneSerializer, DoctorRegisterSerializer, DegreeSerializer, SpecialtySerializer
from Home_module.models import Doctors, Degree, Specialty
from django.core.cache import cache

# Create your views here.
class DoctorsRegView(TemplateView):
    template_name = 'doc-registration.html'

class DegreeApiView(APIView):
    def get(self, request):
        degree = Degree.objects.all()
        serializer = DegreeSerializer(degree, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SpecialtyApiView(APIView):
    def get(self, request, degree_id):
        try:
            degree = Degree.objects.get(id=degree_id)
            specialties = Specialty.objects.filter(degrees=degree)
            serializer = SpecialtySerializer(specialties, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Degree.DoesNotExist:
            return Response({"error": "مدرک یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

class PhoneApiView(APIView):
    def post(self, request):
        step = request.data.get("step")
        phone = request.data.get('phone')
        otp_entered = request.data.get('otp')
        degree = request.data.get('degree')
        specialty = request.data.get('specialty')

        if step == "send_otp":
            # ارسال OTP
            serializer = PhoneSerializer(data={"phone": phone})
            if not serializer.is_valid():
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

            otp = random.randint(10000, 99999)
            cache.set(f"otp_{phone}", otp, timeout=120)
            print(f"OTP: {otp}")
            return Response({"success": True, "message": "OTP ارسال شد."}, status=HTTP_200_OK)

        elif step == "verify_otp":
            # تأیید OTP
            otp_cached = cache.get(f"otp_{phone}")
            if not otp_cached or str(otp_cached) != str(otp_entered):
                return Response({"error": "کد تأیید اشتباه است یا منقضی شده."}, status=HTTP_400_BAD_REQUEST)

            return Response({"success": True, "message": "کد تأیید صحیح است."}, status=HTTP_200_OK)

        elif step == "register":
            # ثبت‌نام پزشک
            doctor_data = request.data.copy()
            doctor_data.pop("otp", None)
            doctor_serializer = DoctorRegisterSerializer(data=doctor_data)



            if doctor_serializer.is_valid():
                try:
                    degree = Degree.objects.get(id=degree)
                    degree_name = degree.name
                except Degree.DoesNotExist:
                    return Response({'error':'مدرک موجود نی'}, status=status.HTTP_404_NOT_FOUND)
                try:
                    specialty = Specialty.objects.get(id=specialty)
                    specialty_name = specialty.name
                except Specialty.DoesNotExist:
                    return Response({'error':'تخصص موجود نی'}, status=status.HTTP_404_NOT_FOUND)
                doctor= Doctors.objects.create(
                    phone=phone,
                    name=doctor_data.get('first_name'),
                    last_name=doctor_data.get('last_name'),
                    id_code=doctor_data.get("national_id"),
                    birthday=doctor_data.get("birth_date"),
                    number=doctor_data.get("medical_id"),
                    sex=doctor_data.get("gender"),
                    degree=degree,
                    degree_name=degree_name,
                    speciality_name=specialty_name,
                )

                return Response({"success": True, "message": "ثبت‌نام با موفقیت انجام شد."}, status=HTTP_200_OK)
            else:
                return Response(doctor_serializer.errors, status=HTTP_400_BAD_REQUEST)

        return Response({"error": "مرحله معتبر نیست."}, status=HTTP_400_BAD_REQUEST)







