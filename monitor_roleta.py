import requests
import time
import json
import os

URL_DA_API = "https://jonbet.bet.br/api/singleplayer-originals/originals/roulette_games/current/1"

# Na Render, não vamos salvar em arquivo, vamos ver a saída nos Logs.
# Mas deixaremos a função de escrita para referência.
NOME_ARQUIVO_SAIDA = "resultados_locais.txt" 

def mapear_cor(cor_id):
    if cor_id == 1: return "Vermelho"
    if cor_id == 2: return "Preto"
    if cor_id == 0: return "Branco"
    return "Desconhecida"

def monitorar():
    ultimo_id_processado = None
    print("✅ [RENDER] Iniciando monitoramento...")

    while True:
        try:
            # O timeout é importante para não deixar o script travado
            resposta = requests.get(URL_DA_API, timeout=15)

            if resposta.status_code == 200:
                dado_atual = resposta.json()
                id_atual = dado_atual.get("id")
                numero_sorteado = dado_atual.get("roll")
                cor_id = dado_atual.get("color")

                if id_atual and id_atual != ultimo_id_processado and numero_sorteado is not None and cor_id is not None:
                    cor_texto = mapear_cor(cor_id)
                    linha_resultado = f"Número: {numero_sorteado} | Cor: {cor_texto}"

                    # Na Render, o principal é ver a saída no Log
                    print(f"💰 Novo resultado: {linha_resultado}")

                    # Também salvamos em um arquivo local, mas ele pode ser temporário
                    with open(NOME_ARQUIVO_SAIDA, 'a', encoding='utf-8') as f:
                        f.write(linha_resultado + "\n")

                    ultimo_id_processado = id_atual
                else:
                    # Isso nos diz que o script está vivo, mas não houve resultado novo
                    print(f"🔄 Verificando... ID atual: {id_atual}. Aguardando resultado final.")

            else:
                print(f"⚠️ Resposta da API não foi 200, foi {resposta.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro de conexão: {e}")
        except Exception as e:
            print(f"💥 Erro inesperado: {e}")

        # Pausa de 10 segundos
        time.sleep(10)

if __name__ == "__main__":
    monitorar()