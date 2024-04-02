from django.contrib import admin
from django.urls import path, include
from customers.views import login, register, redirection

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', redirection, name="redirection"),
    path('login', login, name="login"),
    path('register', register, name="register"),
    path('', include("customers.urls")),
] 
