import os

import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

application = ProtocolTypeRouter({
  "http": AsgiHandler(),
  # We will add WebSocket protocol later, but for now it's just HTTP.
})