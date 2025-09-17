from django.shortcuts import render, redirect
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
            return redirect('/')

def login_adm(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login_adm.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        usuario = auth.authenticate(username=username, password=senha)

        if not usuario:
            messages.error(request, 'Username ou senha inválidos!')
            return redirect('/usuario/login_adm')

        if not usuario.perfil.adm:
            messages.error(request, 'Este usuário não é administrador.')
            return redirect('/usuario/login_adm')

        auth.login(request, usuario)
        return redirect('/home_adm')

        

def sair(request):
    auth.logout(request)
    return redirect('/usuario/login')