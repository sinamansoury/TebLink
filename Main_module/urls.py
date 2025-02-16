from django.urls import path

from Main_module import views

urlpatterns =[
    path('', views.MainView.as_view(), name='main'),
    path('api/consultant/', views.ConsultantApiView.as_view(), name='consultant'),
]