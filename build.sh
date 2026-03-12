#!/bin/bash
# build.sh - script para deploy en Render

echo "🔹 Iniciando deploy de Barbería Django en Render..."

# 1. Activar entorno virtual (opcional, Render lo maneja)
# source venv/bin/activate

# 2. Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Aplicar migraciones
echo "🗄 Aplicando migraciones..."
python manage.py migrate

# 4. Colectar archivos estáticos
echo "🖼 Colectando archivos estáticos..."
python manage.py collectstatic --noinput

# 5. Comprobar la configuración de Django
echo "✅ Verificando la configuración de Django..."
python manage.py check

# 6. Iniciar Gunicorn
#echo "🚀 Iniciando Gunicorn..."
#exec gunicorn barberia_system.wsgi:application --bind 0.0.0.0:$PORT