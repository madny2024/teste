# Importa as bibliotecas necessárias
import requests
import json
from http.server import BaseHTTPRequestHandler

# URL da API original
URL_ORIGINAL = "https://jonbet.bet.br/api/singleplayer-originals/originals/roulette_games/current/1"

def mapear_cor(cor_id):
    """Converte o número da cor em texto."""
    if cor_id == 1:
        return "Vermelho"
    elif cor_id == 2:
        return "Preto"
    elif cor_id == 0:
        return "Branco"
    return "Desconhecida"

# Esta é a função principal que a Vercel vai executar a cada requisição
class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # 1. Busca os dados da API original NA HORA
            resposta = requests.get(URL_ORIGINAL, timeout=10)
            resposta.raise_for_status() # Lança um erro se a requisição falhar
            dado_bruto = resposta.json()

            # 2. Extrai e formata os dados
            resultado_formatado = {
                'numero': dado_bruto.get("roll"),
                'cor': mapear_cor(dado_bruto.get("color")),
                'id_rodada': dado_bruto.get("id"),
                'timestamp': dado_bruto.get("created_at")
            }

            # 3. Envia a resposta de volta como um JSON limpo
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Converte o dicionário Python para uma string JSON
            self.wfile.write(json.dumps(resultado_formatado).encode('utf-8'))

        except Exception as e:
            # Em caso de erro, envia uma mensagem de erro
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            erro_json = { "erro": "Nao foi possivel buscar os dados da API original.", "detalhes": str(e) }
            self.wfile.write(json.dumps(erro_json).encode('utf-8'))
            
        return