import json
import os

from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="")

# Arquivo onde a contagem é persistida em disco
ARQUIVO_CONTAGENS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contagens.json")


def carregar_contagens():
    """Lê o arquivo JSON de contagens do disco, se ele existir."""
    if os.path.exists(ARQUIVO_CONTAGENS):
        try:
            with open(ARQUIVO_CONTAGENS, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def salvar_contagens():
    """Grava o estado atual das contagens no disco."""
    with open(ARQUIVO_CONTAGENS, "w", encoding="utf-8") as f:
        json.dump(contagem_valores, f, ensure_ascii=False, indent=2)


contagem_valores = carregar_contagens()


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

    # Incrementa a contagem para esse valor específico
    contagem_valores[valor] = contagem_valores.get(valor, 0) + 1
    salvar_contagens()

    return jsonify({
        "valor": valor,
        "quantidade": contagem_valores[valor]
    })


@app.route("/api/contagens", methods=["GET"])
def listar_contagens():
    """Endpoint auxiliar: lista todas as contagens registradas (útil para depuração)."""
    return jsonify(contagem_valores)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)