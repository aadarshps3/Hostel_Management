from django.contrib import admin
from django.urls import path

from accounts import views

urlpatterns = [

    path('', views.home, name='home'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('select_role', views.select_role, name='select_role'),
    # path('admin_register/', views.admin_register, name='admin_register'),
    path('student_register/', views.student_register, name='student_register'),
    path('parent_register/', views.parent_register, name='parent_register'),






]
