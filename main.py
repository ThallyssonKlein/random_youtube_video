import random
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Substitua pela sua chave de API e ID do canal:
API_KEY = os.getenv("API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def sortear_video_do_canal():
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Define a busca inicial (máximo de 50 resultados por consulta)
    request = youtube.search().list(
        part="snippet",
        channelId=CHANNEL_ID,
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
    sortear_video_do_canal()