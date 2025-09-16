from django.urls import path
from . import views

#rota , chama a view, nome da rota
urlpatterns = [
    path('ver_chamados/', views.ver_chamados, name="ver_chamados"),
    path('', views.fazer_chamado, name="fazer_chamado"),
]