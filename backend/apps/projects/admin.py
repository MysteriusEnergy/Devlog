from django.contrib import admin
from .models import Project

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']