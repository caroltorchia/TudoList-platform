from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from .forms import RegisterForm, LoginForm
from django.template import RequestContext
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.http import JsonResponse
import json


def index(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  
            user.save()
            request.session['user_email'] = user.email
            return redirect('enviar_codigo')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'register/registro.html', {'form': form})


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  
            user.save()
            request.session['user_email'] = user.email
            return redirect('enviar_codigo')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'register/registro.html', {'form': form})

def send_verification_code(request):
    user_email = request.session.get('user_email', None)  
    if not user_email:
        messages.error(request, 'Endereço de e-mail não encontrado.')
        return redirect('registrar')
    
    code = get_random_string(length=6, allowed_chars='0123456789')
    
    request.session['verification_code'] = code
    
    send_mail(
        'Seu código de verificação',
        f'Por favor, use o seguinte código para verificar sua conta: {code}',
        'from@example.com',
        [user_email],
        fail_silently=False,
    )
    
    return redirect('verificacao_de_codigo')

def confirm_code(request):
    user_email = request.session.get('user_email', None) 
    if request.method == 'POST':
        code_entered = ''.join(request.POST.getlist('code'))
        code_sent = request.session.get('verification_code')
        
        if code_entered == code_sent:
            messages.success(request, 'E-mail verificado com sucesso!')
            return JsonResponse({'success': True})
        else:
            messages.error(request, 'Código inválido. Tente novamente.')
            return JsonResponse({'success': False})
    
    return render(request, 'register/verificacao_de_codigo.html', {'user_email': user_email})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                  login(request, user)
                  return redirect('dashboard')
            else:
                return render(request, 'register/login.html', {'form': form})
    else:
        form = LoginForm()
    
    return render(request, 'register/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')