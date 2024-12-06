
# Importar módulos necesarios para los tests
import os
import django
from django.conf import settings

# Configurar variables específicas para los tests
os.environ['DJANGO_SETTINGS_MODULE'] = 'OfficePack.settings'
django.setup()