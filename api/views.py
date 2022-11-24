from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework import status
from .serializers import (PatientSerializer, DoctorSerializer, AppointmentSerializer)
from .models import (Patient, Doctor, Appointment)



class PatiensAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
   
    
    def get(self, request, format=None):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)

        return Response(serializer.data)


class DoctorsAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
   
    
    def get(self, request, format=None):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)

        return Response(serializer.data)


class AppointmentAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request, format=None):
        if request.method == 'GET':
            appointment = Appointment.objects.filter(user=request.user, status=False).first()
           
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(status = status.HTTP_400_BAD_REQUEST)
                
        
    def post(self, request, format=None):
        code = request.data.get('code', None)
        if code is None:
            return Response({'error':'Invalid data'})
        patient = get_object_or_404(Patient, code=code)
        appointment_qs = Appointment.objects.filter(user=request.user, status=False)
        
        if appointment_qs.exists():
            appointment = appointment_qs[0]
            
            if appointment.doctors.filter(patient__code=patient.code).exists():
                doctor = Doctor.objects.filter(patient=patient,user=request.user, status=False)[0]
               
                doctor.save()
                return Response(status=status.HTTP_200_OK)
            return Response({'massage':'patients does not make an appointment yet'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'You dont have active appointment'}, status=status.HTTP_400_BAD_REQUEST)

class MakeAppointmentAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request, fomart=None):
        code = request.data.get('code', None)
        
        if code is None:
            return Response({'message':'Invalid data'}, status = status.HTTP_400_BAD_REQUEST)
        
        patient = get_object_or_404(Patient, code=code)
        
        doctor_qs = Doctor.objects.filter(patient=patient, user=request.user, status =False)
        if doctor_qs.exists():
            doctor= doctor_qs[0]
            
            doctor.save()
        appointment_qs = Appointment.objects.filter(user=request.user, status=False)
        if appointment_qs.exists():
            appointment = appointment_qs[0]
            if not appointment.doctors.filter(patient__id = doctor.id).exists():
                appointment.doctors.add(doctor)
                return Response(status = status.HTTP_200_OK)
        
        appointmentDate = timezone.now()
        appointment = Appointment.objects.create(user=request.user, appointmentDate=appointmentDate)
        appointment.doctors.add(doctor)
        return Response(status = status.HTTP_200_OK)