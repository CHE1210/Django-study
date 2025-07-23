from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gugudan/', include('core.urls')),  # ← core/urls.py를 include
]