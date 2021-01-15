from django.contrib import admin

from django.contrib import admin
from .models import Project


@admin.register(Project)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'manager', 'text', 'active']
