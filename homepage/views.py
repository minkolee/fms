from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(request, 'homepage/homepage.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            return render(request, 'users/register_success.html')
        else:

            return render(request, 'users/register.html', {'form': form})

    else:
        form = UserCreationForm()
        return render(request, 'users/register.html', {'form': form})
