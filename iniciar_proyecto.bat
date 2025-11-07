@echo off
title  Proyecto ADSO - Inicialización automática
color 0A

echo ============================================
echo    Iniciando entorno Django del Proyecto ADSO
echo ============================================
echo.

REM --- Ruta base del proyecto ---
set BASE_DIR=%~dp0Proyecto_ADSO_integrado\django_project
cd /d "%BASE_DIR%"

REM --- Crear entorno virtual si no existe ---
if not exist "%~dp0venv\Scripts\activate.bat" (
    echo 🔹 No existe entorno virtual. Creándolo...
    python -m venv "%~dp0venv"
)

REM --- Activar entorno virtual ---
call "%~dp0venv\Scripts\activate.bat"

REM --- Instalar dependencias ---
if exist "%~dp0requirements.txt" (
    echo  Instalando dependencias...
    pip install -r "%~dp0requirements.txt"
) else (
    echo  No se encontró requirements.txt. Instalando Django base...
    pip install django psycopg2-binary djangorestframework
)

REM --- Ejecutar migraciones ---
echo  Ejecutando migraciones...
python manage.py makemigrations
python manage.py migrate

REM --- Levantar servidor ---
echo 🚀 Iniciando servidor local en http://127.0.0.1:8000
python manage.py runserver

pause

