from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Project, ProjectFinanceInitialDetail, ProjectBudget
from .forms import ProjectForm, ProjectInitialDetailForm, ProjectBudgetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def project_list(request):
    projects = Project.objects.all()
    quantity = Project.objects.count()
    return render(request, 'projects/project_list.html', {'projects': projects, 'quantity': quantity})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    return render(request, 'projects/project_detail.html', {'project': project})


@login_required
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


@login_required
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


@login_required
def delete_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return redirect('projects:project_list')
    else:
        return redirect('projects:project_list')


@login_required
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


@login_required
def budget(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    budgets = ProjectBudget.objects.all().filter(project__id=project_id).filter(is_virtual=False)
    # 非虚拟条目数量
    quantity = budgets.count()
    # 虚拟条目数量
    quantity_virtual = ProjectBudget.objects.filter(project__id=project_id).filter(is_virtual=True).count()
    return render(request, 'projects/project_budget.html',
                  {'budgets': budgets, 'quantity': quantity, 'project_id': project_id,
                   'project': project, 'show_all': False, 'quantity_virtual': quantity_virtual})


@login_required
def budget_show_all(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    budgets = ProjectBudget.objects.all().filter(project__id=project_id)
    quantity = budgets.count()
    quantity_virtual = ProjectBudget.objects.filter(project__id=project_id).filter(is_virtual=True).count()
    return render(request, 'projects/project_budget.html',
                  {'budgets': budgets, 'quantity': quantity, 'project_id': project_id,
                   'project': project, 'show_all': True, 'quantity_virtual': quantity_virtual})


@login_required
def budget_add(request, project_id):
    if request.method == "GET":
        project = get_object_or_404(Project, id=project_id)
        form = ProjectBudgetForm()
        return render(request, 'projects/project_budget_add.html',
                      {'form': form, 'project_id': project_id, 'project': project})

    else:
        form = ProjectBudgetForm(request.POST)
        project = get_object_or_404(Project, id=project_id)
        is_virtual = request.POST.get("is_virtual")

        if form.is_valid():
            current_object = form.save(commit=False)
            current_object.project = project
            if is_virtual:
                current_object.is_virtual = True
            current_object.save()
            messages.success(request, '成功添加预算条目')
            if is_virtual:
                return redirect(reverse('projects:project_budget_show_all', args=[project_id, ]))
            else:
                return redirect(reverse('projects:project_budget', args=[project_id, ]))
        else:
            return render(request, 'projects/project_budget_add.html',
                          {'form': form, 'project_id': project_id, 'project': project})


@login_required
def budget_edit(request, budget_id):
    if request.method == "GET":
        budget_object = get_object_or_404(ProjectBudget, id=budget_id)
        form = ProjectBudgetForm(instance=budget_object)

        return render(request, 'projects/project_budget_edit.html',
                      {'form': form, 'budget_id': budget_id, 'project_id': budget_object.project.id,
                       'budget': budget_object})

    else:
        budget_object = get_object_or_404(ProjectBudget, id=budget_id)
        form = ProjectBudgetForm(request.POST, instance=budget_object)
        is_virtual = request.POST.get("is_virtual")
        if form.is_valid():
            current_object = form.save(commit=False)
            project_id = int(request.POST.get('project_id'))
            current_object.project = get_object_or_404(Project, id=project_id)
            if is_virtual:
                current_object.is_virtual = True
            else:
                current_object.is_virtual = False
            current_object.save()
            messages.success(request, '成功编辑预算条目:' + budget_object.cost_type)
            if is_virtual:
                return redirect(reverse('projects:project_budget_show_all', args=[project_id, ]))
            else:
                return redirect(reverse('projects:project_budget', args=[project_id, ]))
        else:
            return render(request, 'projects/project_budget_edit.html',
                          {'budget_id': budget_id, 'form': form, 'project_id': budget_object.project.id,
                           'budget': budget_object})


@login_required
def budget_delete(request, project_id, budget_id):
    budget_object = get_object_or_404(ProjectBudget, id=budget_id)
    name = budget_object.cost_type
    budget_object.delete()
    messages.success(request, "已删除预算条目：" + name)
    return redirect(reverse('projects:project_budget', args=[project_id, ]))
