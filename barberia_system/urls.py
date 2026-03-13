from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # login de django
    path('accounts/', include('django.contrib.auth.urls')),

    # urls de la app barberia
    path('', include('barberia.urls')),
]