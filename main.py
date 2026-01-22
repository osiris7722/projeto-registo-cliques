from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
from datetime import datetime
import csv
import os

app = Flask(__name__)

# Função para ligar à base de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar a tabela se não existir
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
    data_input = request.json
    botao_nome = data_input.get('botao')
    
    # Obter data e hora atuais
    agora = datetime.now()
    data_atual = agora.strftime('%d/%m/%Y')
    hora_atual = agora.strftime('%H:%M')

    conn = get_db_connection()
    
    # Lógica do contador sequencial diário
    # Conta quantos cliques existem com a data de hoje
    cursor = conn.execute("SELECT COUNT(*) FROM cliques WHERE data = ?", (data_atual,))
    total_hoje = cursor.fetchone()[0]
    novo_sequencial = total_hoje + 1

    # Guardar no SQLite
    conn.execute("INSERT INTO cliques (botao, sequencial, data, hora) VALUES (?, ?, ?, ?)",
                 (botao_nome, novo_sequencial, data_atual, hora_atual))
    conn.commit()
    conn.close()

    return jsonify({
        'sequencial': novo_sequencial,
        'data': data_atual,
        'hora': hora_atual
    })

@app.route('/exportar')
def exportar():
    conn = get_db_connection()
    cursor = conn.execute("SELECT botao, sequencial, data, hora FROM cliques")
    rows = cursor.fetchall()
    conn.close()

    # Criar ficheiro CSV para abrir no Excel
    caminho_ficheiro = 'relatorio_cliques.csv'
    with open(caminho_ficheiro, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Botao', 'Sequencial_Diario', 'Data', 'Hora'])
        for row in rows:
            writer.writerow([row['botao'], row['sequencial'], row['data'], row['hora']])

    return send_file(caminho_ficheiro, as_attachment=True)

if __name__ == '__main__':
    init_db()
    # Porta 8080 para evitar conflitos no Mac e Replit
    app.run(host='0.0.0.0', port=8080, debug=True)