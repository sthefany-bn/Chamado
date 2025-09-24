from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from .models import Perfil

def cadastrar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'cadastrar.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.error(request, 'Já existe um usuário com esse username!')
            return redirect('/usuario/cadastrar')
        
        user = User.objects.create_user(username=username, password=senha)
        user.first_name = nome
        user.save()
        
        Perfil.objects.create(user=user, nome_completo=nome)
        
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('/usuario/login')

      
def atualizar(request, id):
    perfil = get_object_or_404(Perfil, id=id)
    
    if request.method == "GET":
        print(request.user.perfil.adm)
        return render(request, 'adm/editar_funcionario.html', {'perfil': perfil})
    
    elif request.method == "POST":
        nome_completo = request.POST.get('nome_completo')
        username = request.POST.get('username')
        
        perfil.nome_completo = nome_completo
        perfil.user.username = username 
        perfil.user.save()
        perfil.save()
        
        if request.user.perfil.adm:
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('ver_funcionarios')
        else:
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('ver_meus_chamados')


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        usuario = auth.authenticate(username=username, password=senha)

        if not usuario:
            messages.error(request, 'Username ou senha inválidos!')
            return redirect('/usuario/login')
        else:
            auth.login(request, usuario)

        if request.user.perfil.adm == True:
            return redirect('ver_chamados')
        else:
            return redirect('/')


def sair(request):
    auth.logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('/usuario/login')