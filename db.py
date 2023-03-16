import psycopg2
import psycopg2.extras
from typing import List, Literal
import os
import json 

class Database(object):
    def __init__(self):
        self.conn = psycopg2.connect(
            database=str(os.environ.get('database')),
            user=str(os.environ.get('user')),
            password=str(os.environ.get('password')),
            host=str(os.environ.get('host')),
            port=str(os.environ.get('port'))
        )
        self.curs = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def __enter__(self):
        return self.curs

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

def add_user(id_tg: int, username: str=None):
    with Database() as curs:
        _SQL = f'INSERT INTO users (id, username) \
                 VALUES ({id_tg}, $${username}$$) \
                 ON CONFLICT DO NOTHING;'
        curs.execute(_SQL)