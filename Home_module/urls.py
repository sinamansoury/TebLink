from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns =[

    path('<str:consultant>/',views.DoctorsView.as_view(),name='home'),
    path('<str:doctor_name>/profile/',views.DoctorReserveView.as_view(),name='doc-reserve'),
    path('api/doctors/<str:consultant>/', views.DoctorsApiView.as_view(), name='doctors'),
    path('api/profile/<str:doctor_name>-<str:doctor_last_name>/', views.DoctorProfileApiView.as_view(), name='doctor-profile'),
    path('api/days/', views.DayApiView.as_view(), name='day'),
    path('api/appointments/', views.AppointmentApiView.as_view(), name='appointment'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)