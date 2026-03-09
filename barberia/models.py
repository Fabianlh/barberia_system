from django.db import models


# =============================
# CLIENTE
# =============================

class Cliente(models.Model):

    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


# =============================
# BARBERO
# =============================

class Barbero(models.Model):

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
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default="pendiente"
    )

    creado = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.precio:
            self.precio = self.servicio.precio

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cliente} - {self.servicio} - {self.fecha} {self.hora}"