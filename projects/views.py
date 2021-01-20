from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Project, ProjectFinanceInitialDetail
from .forms import ProjectForm, ProjectInitialDetailForm, ProjectBudget
from django.contrib import messages


def project_list(request):
    projects = Project.objects.all()
    quantity = Project.objects.count()
    return render(request, 'projects/project_list.html', {'projects': projects, 'quantity': quantity})


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    return render(request, 'projects/project_detail.html', {'project': project})


def project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            project_initial = ProjectFinanceInitialDetail()
            project_initial.project = project
            project_initial.save()
            messages.success(request, '成功添加项目：' + request.POST.get("name"))
            return redirect('projects:project_list')
        else:
            return render(request, 'projects/project_add.html', {'form': form})

    form = ProjectForm()

    return render(request, 'projects/project_add.html', {'form': form})


def edit_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            current_project = form.save(commit=False)
            current_project.project = project
            current_project.save()
            messages.success(request, '成功修改项目信息')
            return redirect(reverse('projects:project_list'))
        else:
            return render(request, 'projects/project_edit.html', {'form': form, 'project': project})
    else:
        project = get_object_or_404(Project, id=project_id)
        form = ProjectForm(instance=project)
        return render(request, 'projects/project_edit.html', {'form': form, 'project': project})


def delete_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return redirect('projects:project_list')
    else:
        return redirect('projects:project_list')


def edit_initial(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        form = ProjectInitialDetailForm(request.POST, instance=project.detail)
        if form.is_valid():
            current_project = form.save(commit=False)
            current_project.project = project
            current_project.save()
            messages.success(request, '成功修改项目初始金额')

            return redirect(reverse('projects:project_detail', args=[project_id, ]))
        else:
            return render(request, 'projects/project_edit_initial.html', {'form': form, 'project': project})

    else:
        project = get_object_or_404(Project, id=project_id)
        form = ProjectInitialDetailForm(instance=project.detail)
        return render(request, 'projects/project_edit_initial.html', {'form': form, 'project': project})


def budget(request, project_id):
    budgets = ProjectBudget.objects.all().filter(project__id=project_id)
    return render(request, 'projects/project_budget.html', {'budgets': budgets})
