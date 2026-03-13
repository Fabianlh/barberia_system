from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login de Django
    path('accounts/', include('django.contrib.auth.urls')),

    # URLs de la app barberia
    path('', include('barberia.urls')),
]