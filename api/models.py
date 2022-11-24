from django.db import models
from accounts.models import CustomUser
import string
import random

# Create your models here.


def generate_code():
    while True:
        code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30))
        if Patient.objects.filter(code=code).count() == 0:
            break
    
    return code


class Patient(models.Model):
    code =models.CharField(max_length=30, default=generate_code)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    symptoms = models.CharField(max_length=500)
    admitDate = models.DateField(auto_now=True)


    class Meta:
        db_table = 'patients'
        ordering =['-admitDate']

    def __str__(self):
        return f'{self.Patient_First_Name}'


class Doctor(models.Model):
    code =models.CharField(max_length=30, default=generate_code)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department= models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    patient = models.ForeignKey('Patient', related_name='doctors', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table ='doctors'

    def __str__(self):
        return f'{self.user.user_name}'


class Appointment(models.Model):
    code =models.CharField(max_length=30, default=generate_code)
    title = models.CharField(max_length=250)
    appointmentDate=models.DateTimeField(null=False)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)
    doctors = models.ManyToManyField('Doctor')
    


    class Meta:
        db_table = 'appointments'

    def __str__(self):
        return f'{self.title}'
