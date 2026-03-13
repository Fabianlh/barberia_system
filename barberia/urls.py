from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # dashboard
    path('', views.dashboard, name='dashboard'),

    # login
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # logout
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # reservas
    path('reservar/', views.reservar, name='reservar'),
    path('horas-disponibles/', views.horas_disponibles, name='horas_disponibles'),

    # agenda
    path('agenda/', views.agenda, name='agenda'),

    path('cancelar/<int:cita_id>/', views.cancelar_cita, name='cancelar_cita'),
    path('atendida/<int:cita_id>/', views.marcar_atendida, name='marcar_atendida'),

    path('calendario/', views.calendario, name='calendario'),
    path('citas-json/', views.citas_json, name='citas_json'),

    path('panel-barbero/', views.panel_barbero, name='panel_barbero'),
    path('mover-cita/', views.mover_cita, name='mover_cita'),

    path('estadisticas-chart/', views.estadisticas_chart, name='estadisticas_chart'),
    path('confirmacion/', views.confirmacion, name='confirmacion'),
]