import sys
import psycopg2
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from NEXUS import settings

conn = psycopg2.connect(settings.DATABASES['default'])
cur = conn.cursor()
cur.execute("SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE conrelid = 'projects'::regclass AND contype='c';")
print('constraints=')
for row in cur.fetchall():
    print(row)
cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='projects';")
print('columns=')
for row in cur.fetchall():
    print(row)
cur.close()
conn.close()
