from contextlib import contextmanager

import psycopg2

from core.config import settings


@contextmanager
def get_connection():
    conn = psycopg2.connect(settings.db_url, connect_timeout=5)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
