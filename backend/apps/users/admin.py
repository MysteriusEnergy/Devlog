from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.

@admin.register(User)
class userAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'is_staff', 'created_at']
    ordering = ['-created_at']