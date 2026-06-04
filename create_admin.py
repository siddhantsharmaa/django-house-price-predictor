import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hpp_project.settings')
django.setup()

from django.contrib.auth.models import User

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@gmail.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin')

# ✅ Sirf tab banao jab exist na kare
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username = username,
        email    = email,
        password = password
    )
    print(f"✅ Admin created: {username}")
else:
    print(f"✅ Admin already exists: {username}")