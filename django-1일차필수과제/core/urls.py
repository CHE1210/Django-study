from django.urls import path
from . import views

urlpatterns = [
    path('', views.gugudan_all, name='gugudan_all'),
]