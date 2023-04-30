from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('generate/<int:start>/<int:end>', generate),
    path('monitor/<int:k>', monitor),
    path('get/', get)
]