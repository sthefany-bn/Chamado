from django.urls import path
from . import views

urlpatterns = [
     path('cadastrar/', views.cadastrar, name="cadastrar"),
     path('login/', views.login, name="login"),
     path('sair/', views.sair, name="sair"),
]
