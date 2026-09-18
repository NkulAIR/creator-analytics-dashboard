"""
Patreon OAuth 2.0 credential handling.

Patreon requires a full OAuth authorization-code flow for all data,
even the creator's own campaign info meaning there's no public/app-token
like Twitch and the others.
"""
import os
import pickle
import webbrowser
from urllib.parse import urlencode

import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, "patreon_token.pickle")

PATREON_CLIENT_ID = os.environ["PATREON_CLIENT_ID"]
PATREON_CLIENT_SECRET = os.environ["PATREON_CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:3000"
SCOPES = "identity campaigns campaigns.members"

AUTH_URL = "https://www.patreon.com/oauth2/authorize"
TOKEN_URL = "https://www.patreon.com/api/oauth2/token"


def _exchange_code_for_tokens(code: str) -> dict:
    response = requests.post(TOKEN_URL, data={
        "code": code,
        "grant_type": "authorization_code",
        "client_id": PATREON_CLIENT_ID,
        "client_secret": PATREON_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    })
    response.raise_for_status()
    return response.json()


def _refresh_tokens(refresh_token: str) -> dict:
    response = requests.post(TOKEN_URL, data={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": PATREON_CLIENT_ID,
        "client_secret": PATREON_CLIENT_SECRET,
    })
    response.raise_for_status()
    return response.json()


def get_patreon_access_token() -> str:
    tokens = None

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as f:
            tokens = pickle.load(f)

    if tokens and "refresh_token" in tokens:
        tokens = _refresh_tokens(tokens["refresh_token"])
    else:
        params = {
            "response_type": "code",
            "client_id": PATREON_CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPES,
        }
        auth_url = f"{AUTH_URL}?{urlencode(params)}"
        print(f"Opening browser for Patreon consent: {auth_url}")
        webbrowser.open(auth_url)

        code = input("Paste the 'code' param from the redirect URL: ")
        tokens = _exchange_code_for_tokens(code)

    with open(TOKEN_PATH, "wb") as f:
        pickle.dump(tokens, f)

    return tokens["access_token"]