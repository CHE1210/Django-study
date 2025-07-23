from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.all_gugudan_view, name='all_gugudan'),
]