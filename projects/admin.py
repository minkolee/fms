from django.contrib import admin

from django.contrib import admin
from .models import Project, ProjectFinanceInitialDetail


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'manager', 'text', 'active']

@admin.register(ProjectFinanceInitialDetail)
class PFIDAdmin(admin.ModelAdmin):
    pass