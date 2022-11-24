from django.contrib import admin

from .models import CustomUser

# Register your models here.

class UserAdmi(admin.ModelAdmin):
    list_display = '__all__'

admin.site.register(CustomUser,)
