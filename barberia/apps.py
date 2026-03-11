from django.apps import AppConfig


class BarberiaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'barberia'

    def ready(self):
        from django.contrib.auth.models import User

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@barberia.com",
                password="admin123"
            )