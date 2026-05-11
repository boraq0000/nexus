import os
import sys
import django
import psycopg2

# Script to inspect Supabase/PostgreSQL tables from Django settings.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NEXUS.settings')
django.setup()
from django.conf import settings

# Get database configuration from Django settings
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
    # Remove None values
    connect_kwargs = {k: v for k, v in connect_kwargs.items() if v}
    conn = psycopg2.connect(**connect_kwargs)
with conn.cursor() as cur:
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;")
    tables = [row[0] for row in cur.fetchall()]
    print('PUBLIC TABLES:')
    for t in tables:
        print('-', t)
    print('\nCHECKS:')
    for t in ['projects','projects_member','investments','investor_ratings','evaluations','users']:
        print(f'{t}:', t in tables)

    print('\nPROJECTS COLUMNS:')
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='projects' ORDER BY ordinal_position;")
    for column_name, data_type in cur.fetchall():
        print('-', column_name, data_type)
conn.close()
