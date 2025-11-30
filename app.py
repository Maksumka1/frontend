from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()
## Control 121
## Worker1 228
## Worker2 153
app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'myapp'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password'),
        port=os.getenv('DB_PORT', 5432)
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM items;')
    items = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(items)

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO items (name, description) VALUES (%s, %s);',
                (data['name'], data['description']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Item created'}), 201

@app.route('/healthz', methods=['GET'])
def healthz():
    return jsonify({'status': 'ok'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

print("Hello world")
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)