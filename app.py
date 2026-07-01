
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="")

# Estrutura de dados em memória: { "valor_recebido": quantidade_de_vezes }
contagem_valores = {}


@app.route("/")
def index():
    """Serve a página principal do frontend."""
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/contar", methods=["POST"])
def contar_valor():
    """
    Recebe um valor via JSON (campo "valor"), incrementa sua contagem
    na estrutura em memória e retorna o total atualizado.
    """
    dados = request.get_json(silent=True)

    if not dados or "valor" not in dados:
        return jsonify({"erro": "Campo 'valor' é obrigatório."}), 400

    valor = str(dados["valor"]).strip()

    if valor == "":
        return jsonify({"erro": "O valor não pode ser vazio."}), 400

    # kncrementa a contagem para esse valor específico
    contagem_valores[valor] = contagem_valores.get(valor, 0) + 1

    return jsonify({
        "valor": valor,
        "quantidade": contagem_valores[valor]
    })


@app.route("/api/contagens", methods=["GET"])
def listar_contagens():
    """Endpoint auxiliar: lista todas as contagens registradas (útil para depuração)."""
    return jsonify(contagem_valores)


if __name__ == '__main__':
    app.run(port=5001, debug=True)