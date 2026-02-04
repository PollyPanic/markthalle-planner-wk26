import sys
import os
import site

BASE_DIR = '/var/www/flaskapp'

site.addsitedir(os.path.join(BASE_DIR, 'venv/lib/python3.13/site-packages'))

sys.path.insert(0, BASE_DIR)

from app import server as application

