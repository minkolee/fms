from django.shortcuts import render, get_object_or_404, reverse, redirect
from .models import Entry
from django.contrib import messages
from projects.models import Project


def entry_list_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    entries = project.project_entries.all()
    quantity = entries.count()
    return render(request, 'entry/entry_list_project.html',
                  {'project': project, 'entries': entries, 'quantity': quantity})
