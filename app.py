# Importação de bibliotecas auxiliares
from flask import Flask, request, jsonify
from collections import deque

from .comm.leitor_dados import LeitorDados

app = Flask(__name__)

historico_medicoes = deque(maxlen=10) # Cria uma lista de capacidade máxima igual a 10

@app.route("/", methods=["POST"])
def reportar_nivel_umidade():
    """Esse trecho é executado quando o Arduino envia dados ao servidor, guarda dados na memória."""
    # Passa os dados enviados pelo Arduino pra um formato que o computador entende
    dados = request.get_json() 
    novo_relatorio = { "nivel_umidade": dados.get("nivel_umidade") } # Captura umidade
    historico_medicoes.append(novo_relatorio) # Adiciona mais um relatório no histórico
    return jsonify({"message": "Dados enviados com sucesso!", "report": novo_relatorio}), 201

@app.route("/", methods=["GET"])
def visualizar_relatorios():
    """Esse trecho é executado quando a aplicação solicita os dados armazenados."""
    if not historico_medicoes: # Verifica se existem dados para exibir
        return jsonify({"message": "Ainda nao ha dados registrados!"}), 200
    else:
        return jsonify(list(historico_medicoes)) # Devolve lista com dados

if __name__ == "__main__":
    l = LeitorDados() # Instancia leitor de dados
    app.run(port=3000) # Executa o programa
    l.start() # Inicia leitura de porta