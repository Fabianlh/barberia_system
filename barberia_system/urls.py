from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # login django
    path('accounts/', include('django.contrib.auth.urls')),

    # app barberia
    path('', include('barberia.urls')),
]

# 🔥 SOLO EN DESARROLLO
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)