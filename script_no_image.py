import requests, time, datetime

LASTFM_USER = "USERNAMEKAMU"
LASTFM_API_KEY = "APIKEYKAMU"
BSKY_HANDLE = "username.bsky.social"
BSKY_PASS = "APPSPASSWORDKAMU"

last_track = None

while True:
    r = requests.get("http://ws.audioscrobbler.com/2.0/", params={
        "method": "user.getrecenttracks",
        "user": "USERNAMEKAMU",
        "api_key": "APIKEYKAMU",
        "format": "json",
        "limit": 1
    }).json()

    track = r["recenttracks"]["track"][0]
    if "@attr" in track and track["@attr"].get("nowplaying") == "true":
        artist = track["artist"]["#text"]
        title = track["name"]
        text = f"🎵 Now Playing: {artist} – {title}"

        if text != last_track: 
            # login Bluesky
            session = requests.post("https://bsky.social/xrpc/com.atproto.server.createSession",
                json={"identifier": "username.bsky.social", "password": "APPSPASSWORDKAMU"}).json()
            headers = {
                "Authorization": f"Bearer {session['accessJwt']}",
                "Content-Type": "application/json"
            }

            post = {
                "repo": "DID AKUN KAMU",
                "collection": "app.bsky.feed.post",
                "record": {
                    "text": text,
                    "createdAt": datetime.datetime.utcnow().isoformat() + "Z"
                }
            }

            requests.post("https://bsky.social/xrpc/com.atproto.repo.createRecord",
                          headers=headers, json=post)
            print("Posted:", text)
            last_track = text

    time.sleep(30)
