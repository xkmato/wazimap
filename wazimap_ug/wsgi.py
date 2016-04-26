__author__ = 'kenneth'

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wazimap_ug.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

