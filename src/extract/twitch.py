"""
Twitch Extractor
Decision: Twitch has some limitiations it does not use the same Google  and cannot be built like the Youtube.
There is 

"""

# 1. Authenticate client by creating HTTP requests structured this way:
# header(s) : Client ID and Authorization key
# payload: the intention
# 2. Two auth flows: one for client credentials and user Oauth token flow for private account data like subscriber count, bits, revenue-related figures

# 3. Twitch video endpoints come bundled with the view count so there's no need to make videos id list and batch fetch the stats.
# 4. Twitch has no public like and comments system. 
# Views are this platforms commodity

from datetime import datetime, timezone
import os

import requests
from dotenv import load_dotenv

from .base import BaseExtractor, ExtractResult

load_dotenv()

class TwitchExtractor(BaseExtractor):
    source_name = "twitch"

    
    def __init__(self, broadcaster_login: str | None = None):
        self.client_id = os.environ["TWITCH_CLIENT_ID"]
        self.client_secret = os.environ["TWITCH_CLIENT_SECRET"]
        self.broadcaster_login = broadcaster_login or os.environ["TWITCH_BROADCASTER_LOGIN"]

        self.access_token = self.get_app_access_token()
        self.headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}",
        }


# 1. Step 1: Authenticate client by creating HTTP requests structured this way:

    def get_app_access_token(self) -> str:
        response = requests.post(
            "https://id.twitch.tv/oauth2/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
            },
        )
        response.raise_for_status()
        return response.json()["access_token"]

    # 2. Get broadcaster ID. Twitch uses broactaster ID as user identifier not username
    def get_broadcaster_id(self) -> str:
        response = requests.get(
            "https://api.twitch.tv/helix/users",
            headers=self.headers,
            params={"login": self.broadcaster_login},
        )
        response.raise_for_status()
        data = response.json()["data"]

        if not data:
            raise ValueError(f"No Twitch user found for login '{self.broadcaster_login}'")

        return data[0]["id"]




    # 3. Get all videos using the broadcaster ID
    def get_all_videos(self, broadcaster_id: str, since: datetime | None = None) -> list[dict]:
        videos = []
        cursor = None

        while True:
            params = {"user_id": broadcaster_id, "first": 100}
            if cursor:
                params["after"] = cursor

            response = requests.get(
                "https://api.twitch.tv/helix/videos",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            data = response.json()

            for video in data["data"]:
                created_at = datetime.fromisoformat(
                    video["created_at"].replace("Z", "+00:00")
                )

                if since is None or created_at >= since:
                    videos.append(video)

            cursor = data.get("pagination", {}).get("cursor")
            if not cursor:
                break

        return videos


    def extract(self, since: datetime | None = None) -> ExtractResult:
        broadcaster_id = self.get_broadcaster_id()
        videos = self.get_all_videos(broadcaster_id, since=since)

        return ExtractResult(
            source=self.source_name,
            extracted_at=datetime.now(timezone.utc),
            records=videos,
        )


if __name__ == "__main__":
    # Quick manual test: python -m src.extract.twitch
    extractor = TwitchExtractor()
    result = extractor.extract()
    print(f"Pulled {len(result.records)} records from {result.source}")
