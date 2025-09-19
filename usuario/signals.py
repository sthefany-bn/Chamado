from django.contrib.auth.models import User
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Perfil

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_superuser('admin', '', 'admin')
        Perfil.objects.create(user=user, nome_completo='Administrador', adm=True)
        print("Usuário admin criado com sucesso!")
