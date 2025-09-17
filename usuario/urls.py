from django.urls import path
from . import views

urlpatterns = [
     path('cadastrar/', views.cadastrar, name="cadastrar"),
     path('login/', views.login, name="login"),
     path('login_adm/', views.login_adm, name="login_adm"),
     path('sair/', views.sair, name="sair"),
]
