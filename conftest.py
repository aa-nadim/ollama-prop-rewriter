import os
import django
from django.conf import settings

# Setup Django's settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoCliApp.settings')
django.setup()

# Add any shared fixtures here if needed