# Contador de Valores

Sistema web simples com frontend (HTML/JS) e backend (Flask) que conta
quantas vezes cada valor enviado foi recebido pelo servidor, desde que
ele foi iniciado.

## Estrutura

```
contador-app/
├── app.py                # Backend Flask (rotas + lógica de contagem)
├── requirements.txt      # Dependências Python
└── static/
    └── index.html         # Frontend (HTML + CSS + JS)
```

## Como rodar

1. Crie um ambiente virtual (opcional, mas recomendado):
   ```
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Rode o servidor:
   ```
   python app.py
   ```

4. Abra o navegador em:
   ```
   http://localhost:5000
   ```

## Como funciona

- O frontend (`static/index.html`) tem uma caixa de texto e um botão.
  Ao clicar em "Enviar" (ou pressionar Enter), o valor digitado é enviado
  via `fetch` (POST) para `/api/contar`.

- O backend (`app.py`) mantém um dicionário Python em memória
  (`contagem_valores`), no formato `{ "valor": quantidade }`, que é
  **persistido em disco** no arquivo `contagens.json` a cada atualização.
  Ao iniciar, o servidor carrega esse arquivo (se existir) e continua a
  contagem de onde parou, ou seja, os dados **não** são zerados ao
  reiniciar o servidor.

- O frontend recebe a resposta e exibe na tela "o valor X já foi recebido
  N vez(es)".

## Endpoints da API

| Método | Rota             | Descrição                                              |
|--------|-------------------|---------------------------------------------------------|
| POST   | `/api/contar`     | Recebe `{ "valor": "..." }` e retorna a contagem atualizada |
| GET    | `/api/contagens`  | (auxiliar) Lista todas as contagens registradas          |

