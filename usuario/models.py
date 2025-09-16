from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    TIPOS_USUARIO = (
        ('ADM', 'Administrador'),
        ('FUNC', 'Funcionário'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=4, choices=TIPOS_USUARIO)
    nome_completo = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nome_completo} ({self.get_tipo_display()})"
