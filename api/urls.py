from django.urls import path,include
from .import views


urlpatterns =[

    path('accounts/', include('accounts.urls')),
    path('patients/', views.PatiensAPI.as_view()),
    path('doctors/', views.DoctorsAPI.as_view()),
    path('appointments/', views.AppointmentAPI.as_view()),
    path('makeapointment/', views.MakeAppointmentAPI.as_view())

]