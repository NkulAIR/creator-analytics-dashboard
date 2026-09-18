"""
Test: Pipeline entry point: runs an extractor, then loads its
output into the raw warehouse table.

Usage: python -m src.run_pipeline
"""

from src.extract.youtube import YouTubeExtractor
from src.extract.twitch import TwitchExtractor
from src.extract.patreon import PatreonExtractor

from src.load.load_raw import load_raw


def main():
    for extractor_cls in [YouTubeExtractor, TwitchExtractor, PatreonExtractor]:
        result = extractor_cls().extract()
        n = load_raw(result)
        print(f"Loaded {n} rows into raw_{result.source}")

        
if __name__ == "__main__":
    main()
