import random
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Dicionário com os canais disponíveis
CANAIS = {
    "1": {
        "nome": "Programador de Sucesso",
        "id": "UCHgQAOkK8EPR01C6VgN6Kzg"  # Substitua pelo ID real do canal
    },
}

# Substitua pela sua chave de API:
API_KEY = os.getenv("API_KEY")

def selecionar_canal():
    print("\nCanais disponíveis:")
    for chave, canal in CANAIS.items():
        print(f"{chave} - {canal['nome']}")
    
    while True:
        escolha = input("\nDigite o número do canal desejado: ")
        if escolha in CANAIS:
            return CANAIS[escolha]["id"]
        print("Opção inválida! Tente novamente.")

def sortear_video_do_canal(channel_id):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Define a busca inicial (máximo de 50 resultados por consulta)
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50,
        order="date"
    )

    videos = []
    while request:
        response = request.execute()
        for item in response["items"]:
            if item["id"]["kind"] == "youtube#video":
                videos.append(item["id"]["videoId"])
        request = youtube.search().list_next(request, response)

    print(f"Quantidade de vídeos encontrados: {len(videos)}")
    if videos:
        escolhido = random.choice(videos)
        print(f"Vídeo sorteado: https://www.youtube.com/watch?v={escolhido}")

if __name__ == "__main__":
    channel_id = selecionar_canal()
    sortear_video_do_canal(channel_id)