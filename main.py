from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cliques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            botao TEXT NOT NULL,
            sequencial INTEGER NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clique', methods=['POST'])
def registar_clique():
    data = request.json
    botao_nome = data.get('botao')
    hoje = datetime.now().strftime('%d/%m/%Y')
    agora = datetime.now().strftime('%H:%M:%S')

    conn = get_db_connection()
    # Reinicia o contador a cada novo dia
    cursor = conn.execute("SELECT COUNT(*) FROM cliques WHERE data = ?", (hoje,))
    total_hoje = cursor.fetchone()[0]
    novo_sequencial = total_hoje + 1

    conn.execute("INSERT INTO cliques (botao, sequencial, data, hora) VALUES (?, ?, ?, ?)",
                 (botao_nome, novo_sequencial, hoje, agora))
    conn.commit()
    conn.close()

    return jsonify({
        'sequencial': novo_sequencial,
        'data': hoje,
        'hora': agora
    })

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000, debug=True)