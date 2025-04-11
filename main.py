import random
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Dicionário com os canais e playlists disponíveis
CANAIS = {
    "1": {
        "nome": "Programador de Sucesso",
        "id": "UCHgQAOkK8EPR01C6VgN6Kzg",  # Substitua pelo ID real do canal
        "tipo": "canal"
    },
    "2": {
        "nome": "Dicionário do Programador",
        "id": "PLVc5bWuiFQ8GgKm5m0cZE6E02amJho94o",  # Substitua pelo ID real da playlist
        "tipo": "playlist"
    },
}

# Substitua pela sua chave de API:
API_KEY = os.getenv("API_KEY")

def selecionar_canal():
    print("\nCanais e Playlists disponíveis:")
    for chave, item in CANAIS.items():
        print(f"{chave} - {item['nome']} ({item['tipo']})")
    
    while True:
        escolha = input("\nDigite o número do canal/playlist desejado: ")
        if escolha in CANAIS:
            return CANAIS[escolha]
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

    return videos

def sortear_video_da_playlist(playlist_id):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )
    
    videos = []
    while request:
        response = request.execute()
        for item in response["items"]:
            videos.append(item["snippet"]["resourceId"]["videoId"])
        request = youtube.playlistItems().list_next(request, response)
    
    return videos

if __name__ == "__main__":
    item_escolhido = selecionar_canal()
    
    if item_escolhido["tipo"] == "canal":
        videos = sortear_video_do_canal(item_escolhido["id"])
    else:
        videos = sortear_video_da_playlist(item_escolhido["id"])
    
    print(f"Quantidade de vídeos encontrados: {len(videos)}")
    if videos:
        escolhido = random.choice(videos)
        print(f"Vídeo sorteado: https://www.youtube.com/watch?v={escolhido}")