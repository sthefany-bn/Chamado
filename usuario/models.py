from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    adm = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome_completo}"
    
    class Meta:
        ordering = ["nome_completo"]
