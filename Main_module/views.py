from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Home_module.models import Doctors
# from Main_module.serializers import  ConsultantSerializer


# Create your views here.
class MainView(TemplateView):
    template_name = 'main.html'

# class ConsultantApiView(APIView):
#     def get(self, request):
#         consultant = Consultant.objects.all()
#         serializer = ConsultantSerializer(consultant, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)