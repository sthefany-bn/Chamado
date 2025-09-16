from django.db import models
from usuario.models import Perfil

# Create your models here.
class Chamado(models.Model):
    titulo = models.CharField(max_length=255)
    data = models.DateTimeField()
    status = models.CharField(default="não_iniciado")
    descricao = models.TextField()
    autor = models.ForeignKey(Perfil, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.titulo)