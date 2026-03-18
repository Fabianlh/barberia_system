from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# =============================
# CLIENTE
# =============================

class Cliente(models.Model):

    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, unique=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.telefono})"


# =============================
# BARBERO
# =============================

class Barbero(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# =============================
# SERVICIO
# =============================

class Servicio(models.Model):

    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    duracion = models.PositiveIntegerField(help_text="Duración en minutos")

    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


# =============================
# CITA
# =============================

class Cita(models.Model):

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("atendida", "Atendida"),
        ("cancelada", "Cancelada"),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE)

    fecha = models.DateField()
    hora = models.TimeField()

    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True
    )

    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default="pendiente"
    )

    notas = models.TextField(blank=True, null=True)

    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("barbero", "fecha", "hora")
        ordering = ["-fecha", "-hora"]

    # 🔥 VALIDACIÓN PRO
    def clean(self):

        if self.fecha and self.hora:

            from django.utils import timezone
            from datetime import datetime

            fecha_hora = datetime.combine(self.fecha, self.hora)
            fecha_hora = timezone.make_aware(fecha_hora)

            if fecha_hora < timezone.now():
                raise ValidationError("No puedes agendar en el pasado")

        # evitar doble reserva
        existe = Cita.objects.filter(
            barbero=self.barbero,
            fecha=self.fecha,
            hora=self.hora
        ).exclude(id=self.id).exists()

        if existe:
            raise ValidationError("Este horario ya está ocupado")

    # 🔥 AUTO PRECIO
    def save(self, *args, **kwargs):

        if self.precio is None and self.servicio:
            self.precio = self.servicio.precio

        self.clean()  # 👈 valida antes de guardar

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente} - {self.servicio} - {self.fecha} {self.hora}"