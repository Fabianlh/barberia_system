from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from django.views.decorators.http import require_POST

from datetime import date, datetime
import json

from .models import Cliente, Cita, Servicio, Barbero


# =============================
# LOGIN
# =============================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "login.html")


# =============================
# LOGOUT
# =============================

def logout_view(request):
    logout(request)
    return redirect("login")


# =============================
# DASHBOARD (ADMIN)
# =============================

@login_required
def dashboard(request):

    hoy = date.today()

    citas_hoy = Cita.objects.filter(fecha=hoy).count()
    clientes = Cliente.objects.count()
    barberos = Barbero.objects.count()

    ingresos = Cita.objects.filter(
        fecha=hoy,
        estado="atendida"
    ).aggregate(total=Sum("servicio__precio"))["total"] or 0

    servicio_top = (
        Cita.objects
        .filter(estado="atendida")
        .values("servicio__nombre")
        .annotate(total=Count("id"))
        .order_by("-total")
        .first()
    )

    citas = Cita.objects.select_related(
        "cliente", "servicio", "barbero"
    ).order_by("-fecha", "-hora")[:10]

    return render(request, "dashboard.html", {
        "hoy": hoy,
        "citas_hoy": citas_hoy,
        "clientes": clientes,
        "barberos": barberos,
        "ingresos": ingresos,
        "servicio_popular": servicio_top["servicio__nombre"] if servicio_top else "No hay datos",
        "citas": citas
    })


# =============================
# PANEL BARBERO
# =============================

@login_required
def panel_barbero(request):

    hoy = date.today()

    citas = Cita.objects.filter(
        fecha=hoy,
        barbero__usuario=request.user
    ).select_related("cliente", "servicio").order_by("hora")

    ingresos = Cita.objects.filter(
        fecha=hoy,
        barbero__usuario=request.user,
        estado="atendida"
    ).aggregate(total=Sum("servicio__precio"))["total"] or 0

    return render(request, "barberia/panel_barbero.html", {
        "citas": citas,
        "hoy": hoy,
        "citas_hoy": citas.count(),
        "ingresos": ingresos,
        "clientes": Cliente.objects.count(),
        "barberos": Barbero.objects.count(),
        "servicio_popular": "En progreso"
    })


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
        fecha_hora = timezone.make_aware(fecha_hora)

        if fecha_hora < timezone.now():
            return render(request, "reservar.html", {
                "error": "No puedes reservar en una fecha pasada",
                "servicios": servicios,
                "barberos": barberos
            })

        cliente, _ = Cliente.objects.get_or_create(
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

        return redirect("confirmacion")

    return render(request, "reservar.html", {
        "servicios": servicios,
        "barberos": barberos
    })


# =============================
# CONFIRMACION
# =============================

def confirmacion(request):
    return render(request, "confirmacion.html")


# =============================
# HORAS DISPONIBLES (AJAX)
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

    disponibles = []
    ahora = timezone.localtime()

    for h in horarios:
        hora_dt = datetime.strptime(f"{fecha} {h}", "%Y-%m-%d %H:%M")
        hora_dt = timezone.make_aware(hora_dt)

        if h not in ocupadas and hora_dt > ahora:
            disponibles.append(h)

    return JsonResponse(disponibles, safe=False)


# =============================
# AGENDA
# =============================

@login_required
def agenda(request):

    citas = Cita.objects.select_related(
        "cliente", "servicio", "barbero"
    ).order_by("fecha", "hora")

    return render(request, "agenda.html", {
        "citas": citas,
        "hoy": date.today()
    })


# =============================
# CANCELAR CITA
# =============================

@login_required
def cancelar_cita(request, cita_id):

    cita = get_object_or_404(Cita, id=cita_id)

    if cita.barbero.usuario != request.user:
        return redirect("dashboard")

    cita.estado = "cancelada"
    cita.save()

    return redirect("agenda")


# =============================
# MARCAR ATENDIDA
# =============================

@login_required
def marcar_atendida(request, cita_id):

    cita = get_object_or_404(Cita, id=cita_id)

    if cita.barbero.usuario != request.user:
        return redirect("dashboard")

    cita.estado = "atendida"
    cita.save()

    return redirect("agenda")


# =============================
# CALENDARIO
# =============================

@login_required
def calendario(request):
    return render(request, "calendario.html")


# =============================
# CITAS JSON
# =============================

@login_required
def citas_json(request):

    citas = Cita.objects.select_related(
        "cliente", "servicio", "barbero"
    )

    eventos = []

    for cita in citas:
        eventos.append({
            "id": cita.id,
            "title": f"{cita.cliente.nombre} - {cita.servicio.nombre}",
            "start": f"{cita.fecha}T{cita.hora.strftime('%H:%M:%S')}",
            "color": (
                "#ffc107" if cita.estado == "pendiente"
                else "#28a745" if cita.estado == "atendida"
                else "#dc3545"
            )
        })

    return JsonResponse(eventos, safe=False)


# =============================
# ESTADISTICAS
# =============================

@login_required
def estadisticas_chart(request):

    datos = (
        Cita.objects.filter(estado="atendida")
        .annotate(dia=TruncDay("fecha"))
        .values("dia")
        .annotate(total=Sum("servicio__precio"))
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


# =============================
# MOVER CITA (DRAG & DROP)
# =============================

@login_required
@require_POST
def mover_cita(request):
    try:
        data = json.loads(request.body)

        cita_id = data.get("id")
        fecha = data.get("fecha")
        hora = data.get("hora")

        cita = get_object_or_404(Cita, id=cita_id)

        existe = Cita.objects.filter(
            barbero=cita.barbero,
            fecha=fecha,
            hora=hora
        ).exclude(id=cita.id).exists()

        if existe:
            return JsonResponse({"error": "Horario ocupado"}, status=400)

        cita.fecha = fecha
        cita.hora = hora
        cita.save()

        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)