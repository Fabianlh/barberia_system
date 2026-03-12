from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home(request):
    return redirect('login')  # redirige al login


urlpatterns = [
    path('admin/', admin.site.urls),

    # login / logout de Django
    path('accounts/', include('django.contrib.auth.urls')),

    # página principal -> login
    path('', home),

    # rutas de la app barberia
    path('barberia/', include('barberia.urls')),
]