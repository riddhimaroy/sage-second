"""
WSGI config for SAGE backend.
Used by gunicorn in production.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sage_backend.settings")
application = get_wsgi_application()
