from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Chamado
from usuario.models import Perfil
from datetime import datetime

@login_required(login_url='/usuario/login/')
def fazer_chamado(request):
    if request.method == "GET":
        return render(request, 'fazer_chamado.html')
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        data = datetime.now()
        status = 'nao_iniciado'
        descricao = request.POST.get('descricao')
        autor = request.user.perfil
        
        chamado = Chamado(
            titulo = titulo,
            data = data,
            status = status,
            descricao = descricao,
            autor = autor
        )
        chamado.save()
        
        messages.success(request, 'Chamado enviado com sucesso!')
        return redirect('ver_meus_chamados')

@login_required(login_url='/usuario/login/')
def editar_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    
    if request.method == "GET":
        return render(request, 'editar_chamado.html', {'chamados': chamado})
    
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        
        chamado.titulo = titulo
        chamado.descricao = descricao
        chamado.save()
        
        messages.success(request, 'Chamado atualizado com sucesso!')
        return redirect('ver_meus_chamados')

@login_required(login_url='/usuario/login/')
def ver_meus_chamados(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    chamado = Chamado.objects.filter(autor=perfil)
    
    ativos = chamado.exclude(status__in=['cancelado', 'finalizado']).count()
    finalizados = chamado.filter(status='finalizado').count()
    cancelados = chamado.filter(status='cancelado').count()
    
    return render(request, 'ver_meus_chamados.html', {'perfil': perfil, 
                                                      'chamados':chamado, 
                                                      'qtd_ativos': ativos,
                                                      'qtd_finalizados': finalizados,
                                                      'qtd_cancelados': cancelados})

@login_required(login_url='/usuario/login/')
def cancelar_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    chamado.status = 'cancelado'
    chamado.save()
    print(chamado)
    return redirect('ver_meus_chamados')


@login_required(login_url='/usuario/login/')
def home_adm(request):
    return render(request, 'adm/home_adm.html')

@login_required(login_url='/usuario/login/')
def ver_chamados(request):
    chamado = Chamado.objects.all()
    qtd = chamado.count()
    finalizados = chamado.filter(status='finalizado')
    cancelados = chamado.filter(status='cancelado')
    print(finalizados)
    return render(request, 'adm/ver_chamado.html', {'chamados': chamado, 'quantidade': qtd})