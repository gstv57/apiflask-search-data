from flask import Flask, request, jsonify
import sqlite3


app = Flask(__name__)

def conectarBanco():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/buscar/dados', methods=['POST'])
def buscar_dados():
    data = request.get_json()
    cpf = data.get('cpf')

    if not cpf:
        conn.close()
        return jsonify({'error': 'CPF não fornecido'}), 400

    conn = conectarBanco()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM DADOS WHERE CPF=?", (cpf,))
    dados = cursor.fetchone()

    if not dados:
        conn.close()
        return jsonify({'error': 'CPF não encontrado'}), 404

    cursor.execute("SELECT * FROM EMAIL WHERE CONTATOS_ID=?", (dados['CONTATOS_ID'],))
    emails = cursor.fetchall()

    cursor.execute("SELECT * FROM ENDERECOS WHERE CONTATOS_ID=?", (dados['CONTATOS_ID'],))
    enderecos = cursor.fetchall()

    cursor.execute("SELECT * FROM PARENTES WHERE CPF_Completo=?", (cpf,))
    parentes = cursor.fetchall()

    cursor.execute("SELECT * FROM PIS WHERE CONTATOS_ID=?", (dados['CONTATOS_ID'],))
    pis = cursor.fetchall()

    cursor.execute("SELECT * FROM PODER_AQUISITIVO WHERE CONTATOS_ID=?", (dados['CONTATOS_ID'],))
    poder_aquisitivo = cursor.fetchall()

    cursor.execute("SELECT * FROM SCORE WHERE CONTATOS_ID=?", (dados['CONTATOS_ID'],))
    score = cursor.fetchall()

    cursor.execute("SELECT * FROM TELEFONE WHERE CONTATOS_ID=?", (dados['CONTATOS_ID'],))
    telefones = cursor.fetchall()

    cursor.execute("SELECT * FROM TSE WHERE CONTATOS_ID=?", (dados['CONTATOS_ID'],))
    tse = cursor.fetchall()

    conn.close()

    dados_retorno = {
        'dados': dict(dados),
        'emails': [dict(email) for email in emails],
        'enderecos': [dict(endereco) for endereco in enderecos],
        'parentes': [dict(parente) for parente in parentes],
        'pis': [dict(pi) for pi in pis],
        'poder_aquisitivo': [dict(pa) for pa in poder_aquisitivo],
        'score': [dict(s) for s in score],
        'telefones': [dict(telefone) for telefone in telefones],
        'tse': [dict(t) for t in tse],
    }

    return jsonify(dados_retorno)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)