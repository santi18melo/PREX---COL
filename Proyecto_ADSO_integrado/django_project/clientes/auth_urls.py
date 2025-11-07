from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    CustomLoginView, CustomLogoutView,
    RegistroUsuarioView, PerfilUsuarioView,
    RegisterView, QuickLoginView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Rutas de API
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas del frontend
    path('', QuickLoginView.as_view(), name='quick_login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),

    # Rutas de restablecimiento de contraseña
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='clientes/password_reset_form.html',
            email_template_name='clientes/password_reset_email.html',
            success_url='/clientes/password-reset/done/'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='clientes/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='clientes/password_reset_confirm.html',
            success_url='/clientes/reset/done/'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='clientes/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
