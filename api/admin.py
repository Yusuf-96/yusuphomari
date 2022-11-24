from django.contrib import admin
from .models import Appointment, Patient, Doctor

# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'appointmentDate', 'description', 'status']
class DoctorAdmin(admin.ModelAdmin):
    list_display =[ 'department', 'status']
class PattientAdmin(admin.ModelAdmin):
    list_display = ['symptoms', 'admitDate']
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Patient, PattientAdmin)
admin.site.register(Doctor, DoctorAdmin)
