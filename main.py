https://www.youtube.com/@oprogramadordesucesso

# Instale antes: pip install google-api-python-client

import random
from googleapiclient.discovery import build

# Substitua pela sua chave de API e ID do canal:
API_KEY = "SUA_CHAVE_DE_API"
CHANNEL_ID = "ID_DO_CANAL"

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