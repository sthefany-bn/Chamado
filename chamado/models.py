from django.db import models
from usuario.models import Perfil

# Create your models here.
class Chamado(models.Model):
    STATUS = (
        ('nao_iniciado', 'Não iniciado'),
        ('em_andamento', 'Em andamento'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )
    
    titulo = models.CharField(max_length=255)
    data = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS, default="nao_iniciado")
    descricao = models.TextField()
    autor = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='autor')
    responsavel = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='responsavel')

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ["-data"] 