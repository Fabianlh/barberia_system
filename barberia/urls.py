from django.urls import path
from . import views

urlpatterns = [

    path('', views.reservar_cita, name='reservar'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('agenda/', views.agenda, name='agenda'),

    path('calendario/', views.calendario, name='calendario'),

    path('citas-json/', views.citas_json, name='citas_json'),

    path('horas-disponibles/', views.horas_disponibles, name='horas'),

    path('panel-barbero/', views.panel_barbero, name='panel_barbero'),

    path('atender-cita/<int:cita_id>/', views.atender_cita, name='atender_cita'),
    path('cita-atendida/<int:cita_id>/', views.marcar_atendida, name='cita_atendida'),
    path('cita-cancelar/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),

    path('chart-ingresos/', views.ingresos_chart, name='chart_ingresos'),

    path('cita-atendida/<int:cita_id>/', views.marcar_atendida, name='marcar_atendida'),
path('cita-cancelar/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
]