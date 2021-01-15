from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm
from django.contrib import messages


def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


def project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '成功添加项目：' + request.POST.get("name"))

            return redirect('projects:project_list')
        else:
            return render(request, 'projects/project_add.html', {'form': form})

    form = ProjectForm()

    return render(request, 'projects/project_add.html', {'form': form})
