from rest_framework import serializers
from .models import Patient, Doctor, Appointment
from accounts.serializers import UserSerializer


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Patient
        fields = ['id', 'code', 'user' 'symptoms', 'admitDate']


class DoctorSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    user = UserSerializer()
    class Meta:
        model = Doctor
        fields = ['id', 'code', 'user' 'patient', 'department', 'status', ]


class AppointmentSerializer(serializers.ModelSerializer):
    doctors = DoctorSerializer(many=True)
    class Meta:
        model = Appointment
        fields = ['id','code','title', 'appointmentDate', 'description', 'status', 'doctors']