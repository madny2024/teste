import requests
import time
import json

URL_DA_API = "https://jonbet.bet.br/api/singleplayer-originals/originals/roulette_games/current/1"

def monitorar():
    ultimo_id_processado = None
    print("✅ [KOYEB] Iniciando monitoramento...")

    while True:
        try:
            resposta = requests.get(URL_DA_API, timeout=15)

            if resposta.status_code == 200:
                dado_atual = resposta.json()
                id_atual = dado_atual.get("id")
                numero_sorteado = dado_atual.get("roll")
                cor_id = dado_atual.get("color")

                if id_atual and id_atual != ultimo_id_processado and numero_sorteado is not None and cor_id is not None:
                    cor_texto = "Vermelho" if cor_id == 1 else "Preto" if cor_id == 2 else "Branco"
                    linha_resultado = f"Número: {numero_sorteado} | Cor: {cor_texto}"
                    print(f"💰 Novo resultado: {linha_resultado}")
                    ultimo_id_processado = id_atual
                else:
                    print(f"🔄 Verificando... Sem resultado novo ou completo.")
            else:
                print(f"⚠️ Resposta da API não foi 200, foi {resposta.status_code}")

        except Exception as e:
            print(f"❌ Erro: {e}")

        time.sleep(10)

if __name__ == "__main__":
    monitorar()
