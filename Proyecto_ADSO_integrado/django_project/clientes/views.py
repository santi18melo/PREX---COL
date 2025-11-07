from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from .models import Usuario
from .serializers import UsuarioSerializer
from .forms import RegistroUsuarioForm, QuickLoginForm


# Vistas para la API
class RegisterView(generics.CreateAPIView):
    serializer_class = UsuarioSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        if 'password' not in data:
            return Response(
                {'error': 'password required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = Usuario.objects.create_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password')
        )
        return Response({'id': user.id, 'username': user.username})


# Vistas para el frontend
class QuickLoginView(FormView):
    template_name = 'clientes/quick_login.html'
    form_class = QuickLoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        remember_me = form.cleaned_data.get('remember_me')
        
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        
        if user is not None:
            login(self.request, user)
            
            # Configurar expiración de sesión si no quiere mantenerla
            if not remember_me:
                self.request.session.set_expiry(0)
            
            messages.success(
                self.request,
                f'¡Bienvenido de nuevo, {user.username}!'
            )
            return super().form_valid(form)
        else:
            messages.error(
                self.request,
                'Usuario o contraseña incorrectos. Por favor intenta de nuevo.'
            )
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)


# Vistas para el frontend
class CustomLoginView(LoginView):
    template_name = 'clientes/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'home'


class RegistroUsuarioView(CreateView):
    model = Usuario
    form_class = RegistroUsuarioForm
    template_name = 'clientes/registro.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Auto login después del registro
        login(self.request, self.object)
        return response


class PerfilUsuarioView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'clientes/perfil.html'
    context_object_name = 'usuario'

    def get_object(self):
        return self.request.user
