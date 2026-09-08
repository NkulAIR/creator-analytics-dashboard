"""
YouTube Data API v3 extractor.

Start here first -- see README build order. Pulls channel-level stats
and per-video engagement metrics (views, likes, comments).

Auth: OAuth 2.0 (google-auth-oauthlib). You'll need a Google Cloud
project with the YouTube Data API v3 enabled, and to run through the
OAuth consent flow once locally to get a refresh token.

Docs: https://developers.google.com/youtube/v3
"""
from datetime import datetime, timezone
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
        #1. List videos for self.channel_id (playlistItems or search.list)
        
        playlist_id = self._get_uploads_playlist_id()
        video_ids = self._get_all_video_ids(playlist_id, since=since)
        # 2. For each video, pull statistics (views, likes, comments) via videos.list
        video_stats = self._get_video_stats(video_ids=video_ids)

        extraction_time = datetime.now(timezone.utc)

        return ExtractResult(source=self.source_name,extracted_at=extraction_time,records=video_stats)

        # video_views =  video_stats['statistics']['viewCount']
        # video_likes =  video_stats['statistics']['likeCount']
        # video_dislikes = videos_stats['statistics']['dislikeCount']




        # 3. If `since` is set, filter to videos published/updated after it
        # 4. Return raw API records as-is -- don't transform here





    def _get_uploads_playlist_id(self) -> str:
        response = self.client.channels().list(
            part="contentDetails",
            id=self.channel_id
        ).execute()

        return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]



    def _get_all_video_ids(self, playlist_id: str, since: datetime) -> list[str]:
        video_ids = []
        next_page_token = None

        while True:
            response = self.client.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in response["items"]:
                published_at = datetime.fromisoformat(
                    item["snippet"]["publishedAt"].replace("Z", "+00:00")
                )


                if since is None or published_at >= since:
                    video_ids.append(item["contentDetails"]["videoId"])

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return video_ids

    def _get_video_stats(self, video_ids: list[str]) -> list[dict]:
        # Instead of looping through every single video. loop through batches of 50

        all_stats = []
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i + 50]
            response = self.client.videos().list(
                part="statistics,snippet",
                id=",".join(batch)
            ).execute()
            all_stats.extend(response["items"])
        return all_stats


if __name__ == "__main__":
    extractor = YouTubeExtractor()
    result = extractor.extract()
    print(f"Pulled {len(result.records)} records from {result.source}")