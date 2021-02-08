from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('home/', views.home, name='dashboard'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('test/', views.test, name='test'),
    path('', views.index, name='homepage'),
]
