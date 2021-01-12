from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(request, 'homepage/homepage.html')


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print('有效')
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            return redirect(reverse('login'))
        else:
            print(form.fields['username'])
            print(form.errors)
            return render(request, 'users/register.html', {'form': form, "error": form.error_messages})

    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})
