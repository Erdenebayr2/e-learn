"""e_Learn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from learn import views

urlpatterns = [
    path('', views.index , name='index'),
    path('lesson/', views.lesson, name='lesson'),
    path('signup/', views.signup, name='signup'),	
    path('account/',views.account, name='account'),
    path('teacher/',views.teacher, name='teacher'),
    path('contact/',views.contact, name='contact'),
    path('log_in/', views.log_in, name='log_in'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_out/', views.log_out, name='log_out'),
]
