import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sua chave de API do Google Cloud
API_KEY = "AIzaSyBSf4V1raoxSfWqj6SLSaN1bNful6oAnsc"  # Sua chave de API fornecida
# O ID do seu mecanismo de pesquisa (CX)
CX_ID = "14fcdaff9b77348ff"  # O ID CX do seu Custom Search Engine

# Função para buscar resultados na web via Google Custom Search API
def buscar_resposta_google(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX_ID}"

    try:
        # Fazendo a requisição para a API do Google
        response = requests.get(url)
        data = response.json()

        # Verificando se a resposta contém resultados
        if 'items' in data:
            # Pegando o "snippet" (trecho) do primeiro item retornado
            resultado = data['items'][0]
            return resultado.get('snippet', 'Desculpe, não encontrei uma resposta relevante.')
        else:
            return "Não encontrei resultados relevantes para sua pergunta."
    except Exception as e:
        return f"Erro ao buscar resultados: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resposta', methods=['POST'])
def resposta():
    texto = request.json.get("texto")
    print(f"Texto recebido: {texto}")

    # Busca se a pergunta envolve "jogo do Corinthians" e faz a busca adequada
    if "jogo" in texto.lower() and "corinthians" in texto.lower():
        resposta = buscar_resposta_google("jogo corinthians resultado")
    else:
        # Para outras perguntas, realiza a busca com o texto informado
        resposta = buscar_resposta_google(texto)

    return jsonify({"resposta": resposta})

if __name__ == '__main__':
    app.run(debug=True)
