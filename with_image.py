import time
import requests
from atproto import Client, models

# 🔑 Konfigurasi
LASTFM_USER = "Your_Username"
LASTFM_API_KEY = "Your_LastFM_Apikey"

BLUESKY_HANDLE = "Your_Handle_Bsky"
BLUESKY_PASSWORD = "Your_bsky_password"

# 🎵 Ambil data Now Playing dari Last.fm
def get_now_playing(user, api_key):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "user.getrecenttracks",
        "user": "Your_Username",
        "api_key": "Your_LastFM_Apikey",
        "format": "json",
        "limit": 1
    }
    resp = requests.get(url, params=params).json()
    track = resp["recenttracks"]["track"][0]
    return track

def main():
    client = Client()
    client.login("Your_Handle_Bsky", "Your_Bsky_Password")

    last_posted = None  # buat cek biar gak dobel

    while True:
        try:
            track = get_now_playing('Your_Lastfm_Username', 'Your_ApikeY')

            artist = track["artist"]["#text"]
            title = track["name"]
            album = track["album"]["#text"]
            cover_url = track["image"][-1]["#text"]

            unique_id = f"{artist}-{title}"  # biar gak dobel post
            if unique_id != last_posted:
                message = f"Recently Played:\nArtist: {artist}\nTitle: {title}\nAlbum: {album}"

                img_data = requests.get(cover_url).content
                upload = client.com.atproto.repo.upload_blob(img_data)

                embed = models.AppBskyEmbedImages.Main(
                     images=[models.AppBskyEmbedImages.Image(
                       image=upload.blob,
                       alt=f"Album cover for {album}"
                    )]
                )

                client.send_post(text=message, embed=embed)
                print("Post sukses:", message)

                last_posted = unique_id

            time.sleep(30)  # cek lagi tiap 30 detik

        except Exception as e:
            print("❌ Error:", e)
            time.sleep(60)

if __name__ == "__main__":
    main()
