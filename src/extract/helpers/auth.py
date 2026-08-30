"""
Shared Google OAuth 2.0 credential handling.

Any extractor that talks to a Google API will use get_google_credentials
"""
import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", ".."))  # helpers -> extract -> src -> root
CLIENT_SECRET_PATH = os.path.join(PROJECT_ROOT, "client_secret.json")
TOKEN_PATH = os.path.join(PROJECT_ROOT, "token.pickle")
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_google_credentials():
    creds = None

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "wb") as f:
            pickle.dump(creds, f)

    return creds