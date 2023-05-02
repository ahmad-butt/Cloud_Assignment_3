from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('invoke/', invoke),
    path('plot_usage/', plot_performance)
]
