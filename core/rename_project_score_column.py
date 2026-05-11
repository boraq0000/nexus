import os
import sys
import django
import psycopg2

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NEXUS.settings')
django.setup()
from django.conf import settings

_db_config = settings.DATABASES['default']
if not isinstance(_db_config, dict):
    raise RuntimeError('Expected DATABASES["default"] to be a dict')

db_config = _db_config
connect_kwargs = {
    'dbname': db_config.get('NAME'),
    'user': db_config.get('USER'),
    'password': db_config.get('PASSWORD'),
    'host': db_config.get('HOST'),
    'port': db_config.get('PORT'),
    'sslmode': 'require' if db_config.get('OPTIONS', {}).get('sslmode') in ('require', 'verify-full', 'verify-ca') else None,
}
if db_config.get('URL'):
    conn = psycopg2.connect(db_config['URL'])
else:
    connect_kwargs = {k: v for k, v in connect_kwargs.items() if v}
    conn = psycopg2.connect(**connect_kwargs)
with conn.cursor() as cur:
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='projects' AND column_name='score';")
    if cur.fetchone():
        print('Renaming projects.score to projects.professor_score')
        cur.execute('ALTER TABLE projects RENAME COLUMN score TO professor_score;')
        conn.commit()
        print('Rename completed')
    else:
        print('Column projects.score not found, no rename needed')
conn.close()
