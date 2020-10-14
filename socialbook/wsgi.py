import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

# from python-dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialbook.settings')

load_dotenv(verbose=True)

application = get_wsgi_application()
