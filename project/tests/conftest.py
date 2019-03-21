import os
import configurations

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Prod")
os.environ.setdefault("DJANGO_SECRET_KEY", "insecure")
configurations.setup()
