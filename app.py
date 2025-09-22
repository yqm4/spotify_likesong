import spotipy
from spotipy.oauth2 import SpotifyOAuth
import math
import time

# -----------------------------------
# 認証情報
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "REDIRECT_URI"
SCOPE = "user-library-read playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative"

# 事前に取得したリフレッシュトークン refresh.pyで取得したtokenをいれてください
REFRESH_TOKEN = "REFRESH_TOKEN"


sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

token_info = sp_oauth.refresh_access_token(REFRESH_TOKEN)
access_token = token_info['access_token']

sp = spotipy.Spotify(auth=access_token)

user_id = sp.current_user()['id']

# バックアップ用プレイリストの名前
playlist_name = "Like Songs"

# プレイリストIDを取得、なければ作成
playlists = sp.current_user_playlists(limit=50)['items']
playlist_id = None
for pl in playlists:
    if pl['name'] == playlist_name:
        playlist_id = pl['id']
        break

if not playlist_id:
    playlist = sp.user_playlist_create(
        user=user_id,
        name=playlist_name,
        public=True,
        description="dev yam4sou"
    )
    playlist_id = playlist['id']
    print("作成したプレイリストID:", playlist_id)
else:
    print("既存のプレイリストID:", playlist_id)

# 定期更新1時間ごと
while True:
    try:
      
        token_info = sp_oauth.refresh_access_token(REFRESH_TOKEN)
        access_token = token_info['access_token']
        sp = spotipy.Spotify(auth=access_token)

        total_liked_songs_response = sp.current_user_saved_tracks(limit=1)
        total_liked_songs = total_liked_songs_response['total']
        print(f"Total liked songs: {total_liked_songs}")

     
        existing_tracks = sp.playlist_tracks(playlist_id)['items']
        if existing_tracks:
            track_uris = [item['track']['uri'] for item in existing_tracks]
            sp.playlist_remove_all_occurrences_of_items(playlist_id, track_uris)
            print(f"Removed {len(track_uris)} tracks before update.")

        batch_size = 50
        num_batches = math.ceil(total_liked_songs / batch_size)

        for i in range(num_batches):
            offset = i * batch_size
            liked_songs_batch = sp.current_user_saved_tracks(limit=batch_size, offset=offset)['items']
            uris_to_add = [item['track']['uri'] for item in liked_songs_batch]

            if uris_to_add:
                sp.playlist_add_items(playlist_id, uris_to_add)
                print(f"Added {len(uris_to_add)} songs (batch {i+1}/{num_batches})")

        print(f"All {total_liked_songs} liked songs synced to '{playlist_name}'.")

    except Exception as e:
        print("Error:", e)

    # 1時間待機
    time.sleep(3600)
