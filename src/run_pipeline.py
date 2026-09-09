"""
Test: Pipeline entry point: runs an extractor, then loads its
output into the raw warehouse table.

Usage: python -m src.run_pipeline
"""
from src.extract.youtube import YouTubeExtractor
from src.load.load_raw import load_raw


def main():
    result = YouTubeExtractor().extract()
    n = load_raw(result)
    print(f"Loaded {n} rows into raw_{result.source}")


if __name__ == "__main__":
    main()