"""Twitch Extractor
Decision: Twitch has some limitiations it does not use the same Google API format and cannot be built like the Youtube ONE.
There is 
"""
# 1. Authenticate client by creating HTTP requests structured this way:
# header(s) : Client ID and Authorization key# payload: the intention
# 2. Two auth flows: one for client credentials and user Oauth token flow for private account data like subscriber count, bits, revenue-related figures
# 3. Twitch video endpoints come bundled with the view count so there's no need to make videos id list and batch fetch the stats.
# 4. Twitch has no public like and comments system. # Views are this platforms commodity

"""Twitch ExtractorDecision: Twitch has some limitiations it does not use the same Google and cannot be built like the Youtube.There is 
"""
# 1. Authenticate client by creating HTTP requests structured this way:# header(s) : Client ID and Authorization key# payload: the intention# 2. Two auth flows: one for client credentials and user Oauth token flow for private account data like subscriber count, bits, revenue-related figures
# 3. Twitch video endpoints come bundled with the view count so there's no need to make videos id list and batch fetch the stats.# 4. Twitch has no public like and comments system. # Views are this platforms commodity
import os
import requests
TWITCH_CLIENT_ID = os.environ["TWITCH_CLIENT_ID"]
TWITCH_CLIENT_SECRET = os.environ["TWITCH_CLIENT_SECRET"]
# 1. Step 1: Authenticate client by creating HTTP requests structured this way:
def get_app_access_token() -> str:
    response = requests.post( 
        "https://id.twitch.tv/oauth2/token", 
        data={ 
            "client_id": TWITCH_CLIENT_ID, 
            "client_secret": TWITCH_CLIENT_SECRET,
            "grant_type": "client_credentials",
              },
    ) 
    response.raise_for_status()
    return response.json()["access_token"]
# 2. Get broadcaster ID. Twitch users ID as user identifier not usernamedef get_broadcaster_id(login: str, token: str) -> str: headers = { "Client-ID": TWITCH_CLIENT_ID, "Authorization": f"Bearer {token}", } response = requests.get( "https://api.twitch.tv/helix/users", headers=headers, params={"login": login}, ) response.raise_for_status() return response.json()["data"][0]["id"]
