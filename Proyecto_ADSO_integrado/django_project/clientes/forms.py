from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar los widgets y ayudas
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Elige un nombre de usuario'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Tu correo electrónico'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Elige una contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirma tu contraseña'
        })

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')


class QuickLoginForm(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingresa tu nombre de usuario',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingresa tu contraseña',
            'autocomplete': 'current-password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        label="Mantener sesión iniciada",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
