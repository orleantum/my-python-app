import time
import os
import psycopg2

def get_db_connection():
    # Ждем, пока база проснется
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host='postgres-db',
                database=os.environ['DB_NAME'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD']
            )
            return conn
        except psycopg2.OperationalError:
            print("Waiting for Database...", flush=True)
            retries -= 1
            time.sleep(2)
    raise Exception("Could not connect to database")

# Создаем таблицу при запуске
conn = get_db_connection()
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, count INTEGER);')
# Вставляем начальное значение, если таблицы пустая
cur.execute('INSERT INTO visits (count) SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM visits);')
conn.commit()
cur.close()
conn.close()

while True:
    conn = get_db_connection()
    cur = conn.cursor()

    # Увеличиваем счетчик
    cur.execute('UPDATE visits SET count = count + 1 RETURNING count;')
    new_count = cur.fetchone()[0]
    conn.commit()

    print(f"Hello! I have been seen {new_count} times (Stored in Postgres).", flush=True)

    cur.close()
    conn.close()
    time.sleep(2)
