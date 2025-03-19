"""
WSGI config for api_sig_rml project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Chemin absolu vers ton projet Django sur PythonAnywhere
path = "/home/IDRISSA/api-sig-rml-final"
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_sig_rml.settings')

application = get_wsgi_application()
