from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Chamado
from usuario.models import Perfil
from datetime import datetime

@login_required(login_url='/usuario/login/')
def fazer_chamado(request):
    if request.method == "GET":
        perfil = Perfil.objects.filter(adm=True)
        return render(request, 'fazer_chamado.html', {'perfil': perfil})
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        data = datetime.now()
        status = 'nao_iniciado'
        descricao = request.POST.get('descricao')
        autor = request.user.perfil
        responsavel_id = request.POST.get('responsavel')
        
        responsavel = get_object_or_404(Perfil, id= responsavel_id)
        
        chamado = Chamado(
            titulo = titulo,
            data = data,
            status = status,
            descricao = descricao,
            autor = autor,
            responsavel = responsavel
        )
        chamado.save()
        
        messages.success(request, 'Chamado enviado com sucesso!')
        return redirect('ver_meus_chamados')

@login_required(login_url='/usuario/login/')
def editar_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    perfil = Perfil.objects.filter(adm=True)
    if request.method == "GET":
        return render(request, 'editar_chamado.html', {'chamados': chamado, 'perfil': perfil})
    
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        responsavel_id = request.POST.get('responsavel')
        
        responsavel = get_object_or_404(Perfil, id= responsavel_id)
        
        chamado.titulo = titulo
        chamado.descricao = descricao
        chamado.responsavel = responsavel
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
    return redirect('ver_meus_chamados')

#ADMs
@login_required(login_url='/usuario/login/')
def ver_chamados(request):
    chamado = Chamado.objects.all()
    status = request.GET.get('status')
    if status:
        chamado = chamado.filter(status=status)
    
    qtd = chamado.count()
    return render(request, 'adm/ver_chamado.html', {'chamados': chamado, 'quantidade': qtd})

@login_required(login_url='/usuario/login/')
def ver_funcionarios(request):
    perfil = Perfil.objects.exclude(user=request.user)
    tipo = request.GET.get('adm')
    if tipo:
        perfil = perfil.filter(adm=tipo)
    qtd = perfil.count()
    return render(request, 'adm/ver_funcionarios.html', {'perfil': perfil, 'quantidade': qtd})

@login_required(login_url='/usuario/login/')
def tornar_adm(request, id):
    perfil = get_object_or_404(Perfil, id=id)
    perfil.adm = True
    perfil.save()
    messages.success(request, f'Usuário {perfil.nome_completo} agora é um administrador!')
    return redirect('ver_funcionarios')

@login_required(login_url='/usuario/login/')
def retirar_adm(request, id):
    perfil = get_object_or_404(Perfil, id=id)
    perfil.adm = False
    perfil.save()
    messages.success(request, f'Usuário {perfil.nome_completo} não é mais um administrador!')
    return redirect('ver_funcionarios')

@login_required(login_url='/usuario/login/')
def ver_minhas_tarefas(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    chamado = Chamado.objects.filter(responsavel=perfil.id)
    qtd = chamado.count()
    return render(request, 'adm/ver_minhas_tarefas.html', {'chamados': chamado, 'quantidade': qtd})

@login_required(login_url='/usuario/login/')
def ver_detalhes(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    return render(request, 'adm/ver_detalhes.html', {'chamados': chamado})