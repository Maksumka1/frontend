from flask import Flask, render_template, request, redirect, Response
import psycopg2
import logging
import os
from prometheus_client import generate_latest, Counter, CONTENT_TYPE_LATEST

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# Метрики
REQUEST_COUNTER = Counter('app_requests_total', 'Total HTTP requests to the app')

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="mydb",
        user="postgres",
        password="password123"
    )
    return conn

@app.route('/')
def index():
    REQUEST_COUNTER.inc()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM person
    WHERE name NOT IN (SELECT link FROM viewed_links)
    """)
    pcs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', pcs=pcs)

@app.route('/mark_viewed', methods=['POST'])
def mark_viewed():
    REQUEST_COUNTER.inc()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM person")
    names = cur.fetchall()
    for name in names:
        try:
            cur.execute("INSERT INTO viewed_links (link) VALUES (%s) ON CONFLICT DO NOTHING", (name[0],))
        except:
            pass
    cur.execute("DELETE FROM person")
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
