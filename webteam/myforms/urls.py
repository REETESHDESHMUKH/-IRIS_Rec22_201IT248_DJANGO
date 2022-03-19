from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="myformHome"),
    path('create/', views.create, name="create"),
    path('preview/<int:id>', views.previewresponse, name="preview"),
    path('formcreated/', views.formcreated, name="formcreated"),
    path('login/', views.login, name="login"),
    path('signin/', views.signin, name="signin"),
    path('logOut/', views.logOut, name="logOut"),
    path('previewform/<int:id>', views.previewform, name="previewform"),
    path('filled/<int:id>', views.filled, name="filled"),
]