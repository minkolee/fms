from django.shortcuts import render, get_object_or_404
from projects.models import Project

from .models import ContractType
from .forms import ContractTypeForm


def contract_list_by_project(request, project_id):
    form = ContractTypeForm()

    return render(request, 'contracts/test.html', {'form': form})
