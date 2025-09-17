from django.urls import path
from . import views

urlpatterns = [
    path('fazer_chamado/', views.fazer_chamado, name="fazer_chamado"),
    path('editar_chamado/<int:id>', views.editar_chamado, name="editar_chamado"),
    path('', views.ver_meus_chamados, name="ver_meus_chamados"),
    path('cancelar_chamado/<int:id>', views.cancelar_chamado, name="cancelar_chamado"),
    
    path('home_adm/', views.home_adm, name="home_adm"),
    path('ver_chamados/', views.ver_chamados, name="ver_chamados"),
    path('ver_chamados_nao_iniciado/', views.ver_chamados, name="ver_chamados_nao_iniciado"),
    path('ver_chamados_em_andamento/', views.ver_chamados, name="ver_chamados_em_andamento"),
    path('ver_chamados_finalizado/', views.ver_chamados, name="ver_chamados_finalizado"),
    path('ver_chamados_cancelado/', views.ver_chamados, name="ver_chamados_cancelado"),
]