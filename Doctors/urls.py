from django.urls import path

from Doctors import views

urlpatterns =[
    path('doc-reg/',views.DoctorsRegView.as_view(),name='doc-reg'),

    path('api/doctor/' , views.PhoneApiView.as_view(),name='api-doctor'),
    path('api/degree/', views.DegreeApiView.as_view(),name='api-degree'),
    path('api/specialty/<int:degree_id>/', views.SpecialtyApiView.as_view(),name='api-specialty'),
]