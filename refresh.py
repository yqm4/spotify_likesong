import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp_oauth = SpotifyOAuth(client_id="client_id",
                        client_secret="client_secret",
                        redirect_uri="redirect_uri",
                        scope="user-library-read playlist-modify-public playlist-modify-private")

auth_url = sp_oauth.get_authorize_url()
print("ブラウザでログイン:", auth_url)
code = input("Redirected URL: ").split("code=")[1].split("&")[0]
token_info = sp_oauth.get_access_token(code)
print("Refresh Token:", token_info['refresh_token'])
