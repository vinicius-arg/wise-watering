# Importação de bibliotecas auxiliares
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from collections import deque

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}) # CORS para desenvolvimento (alterar por segurança)

historico_medicoes = deque(maxlen=10) # Cria uma lista de capacidade máxima igual a 10
acoes_pendentes = deque(maxlen=10) # Cria lista de ações pendentes

numero_medicoes = 0

# Rotas do cliente
@app.route("/", methods=["GET"])
def index():
    """Rota principal da aplicação. Renderiza a página."""
    return render_template("index.html")

@app.route("/api/dados", methods=["GET"])
def visualizar_relatorios():
    """Esse trecho é executado quando a aplicação solicita os dados armazenados."""
    if not historico_medicoes: # Verifica se existem dados para exibir
        return jsonify({"message": "Ainda nao ha dados registrados!"}), 204
    else:
        return jsonify(list(historico_medicoes)), 200 # Devolve lista com dados
    
@app.route("/api/acoes", methods=["POST"])
def solicitar_realizacao_acao():
    """Esse trecho é executado quando o cliente solicita que uma ação seja realizada pelo Arduino."""
    # Passa os dados enviados pelo Arduino pra um formato que o computador entende
    dados = request.get_json() 
    nova_acao = { "type": "action", "data": dados.get("carga") } # Cria ação
    acoes_pendentes.append(nova_acao) # Adiciona mais uma ação na lista
    return jsonify({"message": "Ação solicitada com sucesso!", "acao": nova_acao}), 201


# Rotas do broker
@app.route("/api/acoes", methods=["GET"])
def checar_acoes_pendentes():
    """Esse trecho é executado quando o nó central solicita ações pendentes."""
    if not acoes_pendentes: # Verifica se existem ações
        return jsonify({"message": "Ainda nao ha dados registrados!"}), 204
    else:
        return jsonify(acoes_pendentes.pop()), 200 # Devolve ação mais antiga
    
@app.route("/api/dados", methods=["POST"])
def reportar_nivel_umidade():
    """Esse trecho é executado quando o Arduino envia dados ao servidor, guarda dados na memória."""
    # Passa os dados enviados pelo Arduino pra um formato que o computador entende
    global numero_medicoes
    numero_medicoes+=1 # Incrementa número de medições 
    dados = request.get_json()
    novo_relatorio = { "type": "info", "number": numero_medicoes, "data": dados.get("carga") } # Captura umidade
    historico_medicoes.append(novo_relatorio) # Adiciona mais um relatório no histórico
    return jsonify({"message": "Dados enviados com sucesso!", "report": novo_relatorio}), 201


if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0") # Inicia o servidor
