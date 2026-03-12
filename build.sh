#!/usr/bin/env bash

echo "🔹 Iniciando deploy de Barbería Django en Render..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Migraciones
echo "🗄 Aplicando migraciones..."
python manage.py migrate --noinput

# Archivos estáticos
echo "🖼 Colectando archivos estáticos..."
python manage.py collectstatic --noinput

# Verificar proyecto
echo "✅ Verificando configuración..."
python manage.py check