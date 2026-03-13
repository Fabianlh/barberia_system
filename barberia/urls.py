from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Login / Logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Reservas
    path('reservar/', views.reservar, name='reservar'),
    path('horas-disponibles/', views.horas_disponibles, name='horas_disponibles'),

    # Agenda
    path('agenda/', views.agenda, name='agenda'),

    # Gestión de citas
    path('cancelar/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    path('atendida/<int:cita_id>/', views.marcar_atendida, name='marcar_atendida'),

    # Calendario
    path('calendario/', views.calendario, name='calendario'),
    path('citas-json/', views.citas_json, name='citas_json'),
    path('mover-cita/', views.mover_cita, name='mover_cita'),

    # Panel barbero
    path('panel-barbero/', views.panel_barbero, name='panel_barbero'),

    # Estadísticas
    path('estadisticas-chart/', views.estadisticas_chart, name='estadisticas_chart'),

    # Confirmación
    path('confirmacion/', views.confirmacion, name='confirmacion'),
]