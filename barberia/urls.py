from django.urls import path
from . import views

urlpatterns = [

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Login propio (NO usar auth_views)
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Reservar cita
    path('reservar/', views.reservar_cita, name='reservar'),

    # Horas disponibles
    path('horas-disponibles/', views.horas_disponibles, name='horas_disponibles'),

    # Agenda
    path('agenda/', views.agenda, name='agenda'),

    # Cancelar cita
    path('cancelar/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),

    # Marcar atendida
    path('atendida/<int:cita_id>/', views.marcar_atendida, name='marcar_atendida'),

    # Calendario
    path('calendario/', views.calendario, name='calendario'),

    # Citas JSON
    path('citas-json/', views.citas_json, name='citas_json'),

    # Panel barbero
    path('panel-barbero/', views.panel_barbero, name='panel_barbero'),

    # Mover cita
    path('mover-cita/', views.mover_cita, name='mover_cita'),

    # Estadísticas
    path('estadisticas-chart/', views.estadisticas_chart, name='estadisticas_chart'),

    # Confirmación
    path('confirmacion/', views.confirmacion, name='confirmacion'),
]