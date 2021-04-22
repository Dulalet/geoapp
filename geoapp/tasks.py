import psycopg2
from celery import shared_task
from django.db import connections


# Task для celery для удаления барьеров по времени
@shared_task
def remove_barriers():
    conn = connections['default']
    conn.ensure_connection()
    with conn.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
        cursor.execute("""UPDATE ways
            SET barrier = FALSE
            WHERE barrier = TRUE;""")
    return 'barriers removed'
