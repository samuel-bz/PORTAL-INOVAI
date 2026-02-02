import os
import django
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal_inovai.settings")
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'portal_%';")
    tables = cursor.fetchall()
    print("Portal Tables found in DB:")
    for t in tables:
        print(t[0])
