from django.contrib import admin
from .models import Cliente, Barbero, Servicio, Cita


# =============================
# CLIENTES
# =============================

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre",
        "telefono",
        "creado"
    )

    search_fields = (
        "nombre",
        "telefono"
    )


# =============================
# BARBEROS
# =============================

@admin.register(Barbero)
class BarberoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre",
        "activo"
    )


# =============================
# SERVICIOS
# =============================

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre",
        "precio"
    )


# =============================
# CITAS
# =============================

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "cliente",
        "servicio",
        "barbero",
        "fecha",
        "hora",
        "precio",
        "estado"
    )

    list_filter = (
        "estado",
        "barbero",
        "fecha"
    )

    search_fields = (
        "cliente__nombre",
        "barbero__nombre"
    )