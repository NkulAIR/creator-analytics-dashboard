"""
YouTube Data API v3 extractor.

Start here first -- see README build order. Pulls channel-level stats
and per-video engagement metrics (views, likes, comments).

Auth: OAuth 2.0 (google-auth-oauthlib). You'll need a Google Cloud
project with the YouTube Data API v3 enabled, and to run through the
OAuth consent flow once locally to get a refresh token.

Docs: https://developers.google.com/youtube/v3
"""
from datetime import datetime
import os

from dotenv import load_dotenv
import googleapiclient.discovery
from .base import BaseExtractor, ExtractResult
load_dotenv()

from .helpers.auth import get_google_credentials 

class YouTubeExtractor(BaseExtractor):
    source_name = "youtube"

    def __init__(self, channel_id: str | None = None):
        self.channel_id = channel_id or os.environ["YOUTUBE_CHANNEL_ID"]

        # Authenticated client
        # self.client = googleapiclient.discovery.build("")
    
        self.client = googleapiclient.discovery.build("youtube", "v3", credentials=get_google_credentials())


    def extract(self, since: datetime | None = None) -> ExtractResult:
        """
        TODO:
        1. List videos for self.channel_id (playlistItems or search.list)
        2. For each video, pull statistics (views, likes, comments) via videos.list
        3. If `since` is set, filter to videos published/updated after it
        4. Return raw API records as-is -- don't transform here
        """



        raise NotImplementedError("Implement YouTube API calls here")



        

if __name__ == "__main__":
    # Quick manual test: python -m src.extract.youtube
    extractor = YouTubeExtractor()
    extractor.channel_id
    result = extractor.extract()
    print(f"Pulled {len(result.records)} records from {result.source}")
