from django.urls import path
from . import views

urlpatterns = [
    path('fazer_chamado/', views.fazer_chamado, name="fazer_chamado"),
    path('editar_chamado/<int:id>', views.editar_chamado, name="editar_chamado"),
    path('', views.ver_meus_chamados, name="ver_meus_chamados"),
    path('cancelar_chamado/<int:id>', views.cancelar_chamado, name="cancelar_chamado"),
    path('remover_arquivo/<int:id>', views.remover_arquivo, name="remover_arquivo"),
    path('ver_detalhes/<int:id>', views.ver_detalhes, name="ver_detalhes"),
    
    path('ver_chamados/', views.ver_chamados, name="ver_chamados"),
    path('ver_funcionarios/', views.ver_funcionarios, name="ver_funcionarios"),
    path('tornar_adm/<int:id>', views.tornar_adm, name="tornar_adm"),
    path('retirar_adm/<int:id>', views.retirar_adm, name="retirar_adm"),
    path('ver_minhas_tarefas/', views.ver_minhas_tarefas, name="ver_minhas_tarefas"),
    path('ifc/<int:id>/<str:status>', views.ifc, name="ifc"),   #iniciar, finalizar, cancelar
]