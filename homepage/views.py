from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from .models import About
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from contracts.models import Contract


def index(request):
    return render(request, 'homepage/index.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = True
            new_user.save()
            # 注册成功
            messages.success(request, "注册成功，请登录")
            return render(request, 'users/login.html', {"next": "/"})
        else:
            return render(request, 'users/register.html', {'form': form})

    else:
        form = UserCreationForm()
        return render(request, 'users/register.html', {'form': form})


def about(request):
    abouts = About.objects.all()
    return render(request, 'homepage/about.html', {'abouts': abouts})


@login_required(login_url='/login/?next=home')
def home(request):
    return render(request, 'homepage/dashboard.html')




# 测试简单页面所用
def test(request):
    contract = Contract.objects.all()[0]

    return render(request, 'base/test.html', {'contract': contract})
