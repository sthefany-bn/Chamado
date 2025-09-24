from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Chamado, Arquivo
from usuario.models import Perfil
from datetime import datetime

@login_required(login_url='/usuario/login/')
def fazer_chamado(request):
    if request.method == "GET":
        perfil = Perfil.objects.filter(adm=True).exclude(id=1)
        return render(request, 'fazer_chamado.html', {'perfil': perfil})
    elif request.method == "POST":
        try:
            titulo = request.POST.get('titulo')
            data = datetime.now()
            status = 'nao_iniciado'
            descricao = request.POST.get('descricao')
            autor = request.user.perfil
            responsavel_id = request.POST.get('responsavel')
            arquivos = request.FILES.getlist('arquivos')
        
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
            
            for arquivo in arquivos:
                Arquivo.objects.create(arquivo=arquivo, chamado=chamado)
            
            messages.success(request, 'Chamado enviado com sucesso!')
            return redirect('ver_meus_chamados')
        except:
            messages.success(request, 'Erro ao enviar chamado!')
            return redirect('ver_meus_chamados')


@login_required(login_url='/usuario/login/')
def editar_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    perfil = Perfil.objects.filter(adm=True)
    if request.method == "GET":
        return render(request, 'editar_chamado.html', {'chamados': chamado, 'perfil': perfil})
    
    elif request.method == "POST":
        try:
            titulo = request.POST.get('titulo')
            descricao = request.POST.get('descricao')
            responsavel_id = request.POST.get('responsavel')
            arquivos = request.FILES.getlist('arquivos')
            
            responsavel = get_object_or_404(Perfil, id= responsavel_id)
            
            chamado.titulo = titulo
            chamado.descricao = descricao
            chamado.responsavel = responsavel
            chamado.save()
            
            for arquivo in arquivos:
                Arquivo.objects.create(arquivo=arquivo, chamado=chamado)
            
            messages.success(request, 'Chamado atualizado com sucesso!')
            return redirect('ver_meus_chamados')
        except:
            messages.success(request, 'Erro ao atualizar chamado!')
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
    if chamado.status == 'nao_iniciado':
        chamado.status = 'cancelado'
        chamado.save()
        return redirect('ver_meus_chamados')
    else:
        messages.error(request, 'Esse chamado não pode ser cancelado pois ele já foi iniciado')
        return redirect('ver_meus_chamados')


@login_required(login_url='/usuario/login/')
def remover_arquivo(request, id):
    arquivo = get_object_or_404(Arquivo,id=id)
    arquivo.delete()
    messages.success(request, 'Arquivo deletado com sucesso!')
    
    #Redireciona para a página anterior, se não para ver_meus_chamados
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('ver_meus_chamados')


@login_required(login_url='/usuario/login/')
def ver_detalhes(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    arquivos = chamado.arquivo.all()
    return render(request, 'ver_detalhes.html', {'chamados': chamado, 'arquivos': arquivos})


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
    chamado_ativos = chamado.filter(status__in=['nao_iniciado', 'em_andamento'])
    chamado_inativos = chamado.filter(status__in=['cancelado', 'finalizado'])

    return render(request, 'adm/ver_minhas_tarefas.html', {'chamados_ativos': chamado_ativos, 'chamados_inativos': chamado_inativos})


@login_required(login_url='/usuario/login/')
#ifc = iniciar, finalizar, cancelar
def ifc(request, id, status):
    chamado = get_object_or_404(Chamado, id=id)
    chamado.status = status
    chamado.save()
    return redirect('ver_minhas_tarefas')
