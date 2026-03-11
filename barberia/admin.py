from django.contrib import admin
from .models import Cliente, Servicio, Barbero, Cita


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "telefono")
    search_fields = ("nombre", "telefono")


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio")
    search_fields = ("nombre",)


@admin.register(Barbero)
class BarberoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "servicio",
        "barbero",
        "fecha",
        "hora",
        "precio",
        "estado",
    )

    list_filter = ("estado", "barbero", "fecha")

    search_fields = (
        "cliente__nombre",
        "barbero__nombre",
        "servicio__nombre",
    )

    date_hierarchy = "fecha"