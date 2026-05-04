#!/bin/sh

set -e

echo "Creando migraciones..."
python manage.py makemigrations --noinput

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Cargando datos iniciales..."
python manage.py seed_initial_data

echo "Recolectando archivos estaticos..."
python manage.py collectstatic --noinput

echo "Inicializacion completada."