from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Chamado
from usuario.models import Perfil
from datetime import datetime

@login_required(login_url='/usuario/login/')
def ver_chamados(request):
    chamado = Chamado.objects.all()
    qtd = chamado.count()
    return render(request, 'ver_chamado.html', {'chamados': chamado, 'quantidade': qtd})

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
        return redirect('ver_chamados')

