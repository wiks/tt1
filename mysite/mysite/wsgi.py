"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import logging
logger = logging.getLogger('myproject.custom')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
logger.debug(u'jestem w tt1.mysite.wsgi.py')
application = get_wsgi_application()
