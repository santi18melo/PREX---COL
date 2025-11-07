# ==========================================
# Script de inicialización automática
# Proyecto ADSO - Versión Django + SQLite
# ==========================================

Write-Host " Iniciando configuración automática del Proyecto ADSO..." -ForegroundColor Cyan

# Verificar que Python esté instalado
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host " Python no está instalado o no está en PATH." -ForegroundColor Red
    Write-Host "Descarga Python desde https://www.python.org/downloads/ y vuelve a ejecutar este script."
    exit
}

# Buscar manage.py en subcarpetas
$projectRoot = Get-Location
$managePath = Get-ChildItem -Path $projectRoot -Recurse -Filter "manage.py" -ErrorAction SilentlyContinue | Select-Object -First 1

if (-not $managePath) {
    Write-Host " No se encontró el archivo manage.py. Asegúrate de estar en la carpeta del proyecto." -ForegroundColor Red
    exit
}

$projectDir = Split-Path $managePath.FullName
Set-Location $projectDir
Write-Host " Proyecto localizado en: $projectDir"

# Crear entorno virtual si no existe
if (!(Test-Path -Path "venv")) {
    Write-Host " Creando entorno virtual..."
    python -m venv venv
}

# Activar entorno virtual
Write-Host " Activando entorno virtual..."
$env:VIRTUAL_ENV_DISABLE_PROMPT = "1"
cmd /c "venv\Scripts\activate.bat && echo entorno activado"

# Actualizar pip e instalar dependencias
Write-Host " Instalando dependencias..."
python -m pip install --upgrade pip
if (Test-Path -Path "requirements.txt") {
    pip install -r requirements.txt
} else {
    Write-Host " No se encontró requirements.txt. Se instalarán paquetes esenciales."
    pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary
}

# Usar SQLite temporalmente
$env:DJANGO_USE_SQLITE = "True"

# Aplicar migraciones
Write-Host " Aplicando migraciones..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Crear superusuario automático si no existe
Write-Host " Verificando superusuario..."
$checkAdmin = python manage.py shell -c "from django.contrib.auth import get_user_model; print(get_user_model().objects.filter(username='admin').exists())"
if ($checkAdmin -eq "False") {
    Write-Host " Creando superusuario admin / admin123..."
    python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.create_superuser('admin','admin@example.com','admin123')"
}

# Ejecutar servidor
Write-Host " Iniciando servidor de desarrollo..."
python manage.py runserver

