from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncDay
from datetime import date, datetime

from .models import Cliente, Cita, Servicio, Barbero


# =============================
# DASHBOARD ADMIN
# =============================

@login_required
def dashboard(request):

    hoy = date.today()

    citas_hoy = Cita.objects.filter(fecha=hoy).count()
    total_clientes = Cliente.objects.count()
    total_barberos = Barbero.objects.count()

    ingresos_hoy = Cita.objects.filter(
        fecha=hoy,
        estado="atendida"
    ).aggregate(total=Sum("precio"))["total"] or 0

    ingresos_mes = Cita.objects.filter(
        fecha__month=hoy.month,
        estado="atendida"
    ).aggregate(total=Sum("precio"))["total"] or 0

    # servicio más vendido
    servicio_top = (
        Cita.objects.filter(estado="atendida")
        .values("servicio__nombre")
        .annotate(total=Sum("precio"))
        .order_by("-total")
        .first()
    )

    # barbero con más citas
    barbero_top = (
        Cita.objects.filter(estado="atendida")
        .values("barbero__nombre")
        .annotate(total=Sum("precio"))
        .order_by("-total")
        .first()
    )

    citas = Cita.objects.select_related(
        "cliente",
        "servicio",
        "barbero"
    ).order_by("-fecha")[:10]

    context = {
        "citas_hoy": citas_hoy,
        "clientes": total_clientes,
        "barberos": total_barberos,
        "ingresos_hoy": ingresos_hoy,
        "ingresos_mes": ingresos_mes,
        "servicio_top": servicio_top,
        "barbero_top": barbero_top,
        "citas": citas
    }

    return render(request, "dashboard.html", context)

# =============================
# RESERVAR CITA
# =============================

def reservar_cita(request):

    servicios = Servicio.objects.all()
    barberos = Barbero.objects.filter(activo=True)

    if request.method == "POST":

        nombre = request.POST.get("nombre")
        telefono = request.POST.get("telefono")
        servicio_id = request.POST.get("servicio")
        barbero_id = request.POST.get("barbero")
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")

        fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")

        if fecha_hora < timezone.now():
            return render(request, "reservar.html", {
                "error": "No puedes reservar en una fecha pasada",
                "servicios": servicios,
                "barberos": barberos
            })

        cliente, created = Cliente.objects.get_or_create(
            nombre=nombre,
            telefono=telefono
        )

        existe = Cita.objects.filter(
            barbero_id=barbero_id,
            fecha=fecha,
            hora=hora,
            estado__in=["pendiente", "atendida"]
        ).exists()

        if existe:
            return render(request, "reservar.html", {
                "error": "Ese horario ya está ocupado",
                "servicios": servicios,
                "barberos": barberos
            })

        Cita.objects.create(
            cliente=cliente,
            servicio_id=servicio_id,
            barbero_id=barbero_id,
            fecha=fecha,
            hora=hora
        )

        return render(request, "confirmacion.html", {
            "cliente": nombre,
            "telefono": telefono,
            "fecha": fecha,
            "hora": hora
        })

    return render(request, "reservar.html", {
        "servicios": servicios,
        "barberos": barberos
    })


# =============================
# HORAS DISPONIBLES
# =============================

def horas_disponibles(request):

    fecha = request.GET.get("fecha")
    barbero_id = request.GET.get("barbero")

    horarios = [
        "09:00","09:30","10:00","10:30",
        "11:00","11:30","12:00",
        "14:00","14:30","15:00",
        "15:30","16:00","16:30","17:00"
    ]

    citas = Cita.objects.filter(
        fecha=fecha,
        barbero_id=barbero_id,
        estado__in=["pendiente","atendida"]
    ).values_list("hora", flat=True)

    ocupadas = [c.strftime("%H:%M") for c in citas]

    disponibles = [h for h in horarios if h not in ocupadas]

    return JsonResponse(disponibles, safe=False)


# =============================
# CALENDARIO
# =============================

@login_required
def calendario(request):
    return render(request, "calendario.html")


# =============================
# EVENTOS DEL CALENDARIO
# =============================

def citas_json(request):

    citas = Cita.objects.select_related(
        "cliente","servicio","barbero"
    ).all()

    eventos = []

    for cita in citas:

        color = "#3788d8"

        if cita.estado == "atendida":
            color = "#28a745"

        elif cita.estado == "cancelada":
            color = "#dc3545"

        eventos.append({
            "id": cita.id,
            "title": f"{cita.cliente.nombre} - {cita.servicio.nombre}",
            "start": f"{cita.fecha}T{cita.hora}",
            "color": color
        })

    return JsonResponse(eventos, safe=False)


# =============================
# PANEL BARBERO
# =============================

@login_required
def panel_barbero(request):

    citas = Cita.objects.select_related(
        "cliente","servicio"
    ).filter(
        barbero__nombre=request.user.username
    ).order_by("fecha","hora")

    return render(request, "panel_barbero.html", {
        "citas": citas
    })


# =============================
# VER DETALLE CITA
# =============================

@login_required
def atender_cita(request, cita_id):

    cita = get_object_or_404(Cita, id=cita_id)

    return render(request, "barberia/atender_cita.html", {
        "cita": cita
    })


# =============================
# MARCAR ATENDIDA
# =============================

@login_required
def marcar_atendida(request, cita_id):

    cita = get_object_or_404(Cita, id=cita_id)

    cita.estado = "atendida"
    cita.save()

    return redirect("agenda")


# =============================
# CANCELAR CITA
# =============================

@login_required
def cancelar_cita(request, cita_id):

    cita = get_object_or_404(Cita, id=cita_id)

    cita.estado = "cancelada"
    cita.save()

    return redirect("agenda")


# =============================
# AGENDA GENERAL
# =============================

@login_required
def agenda(request):

    citas = Cita.objects.select_related(
        "cliente",
        "servicio",
        "barbero"
    ).all().order_by("fecha","hora")

    contexto = {
        "citas": citas,
        "hoy": date.today()
    }

    return render(request, "agenda.html", contexto)


# =============================
# GRAFICA INGRESOS
# =============================

@login_required
def ingresos_chart(request):

    datos = (
        Cita.objects.filter(estado="atendida")
        .annotate(dia=TruncDay("fecha"))
        .values("dia")
        .annotate(total=Sum("precio"))
        .order_by("dia")
    )

    labels = []
    valores = []

    for d in datos:
        labels.append(d["dia"].strftime("%Y-%m-%d"))
        valores.append(float(d["total"]))

    return JsonResponse({
        "labels": labels,
        "valores": valores
    })