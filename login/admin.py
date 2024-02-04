from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('fullaname', 'email', 'created_at', 'updated_at', 'is_staff')
    search_fields = ('fullaname', 'email')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(CustomUser, CustomUserAdmin)
