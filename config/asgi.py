import os

import eventlet
import eventlet.wsgi
import socketio
from django.core.asgi import get_asgi_application

from apps.users.consumers import sio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

django_application = get_asgi_application()

application = socketio.ASGIApp(sio, django_application)
