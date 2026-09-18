"""
Full pipeline: extract, load, and transform all platforms in sequence.

Includes basic logging and a lock file feature to prevent overlapping runs
: when a scheduled run is still going when the next trigger fires

Full orchestration (retries, per-task failure isolation, alerting,
run history) is deliberately deferred to future Airflow implementation

Usage: python -m src.run_all
"""
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from src.extract.youtube import YouTubeExtractor
from src.extract.twitch import TwitchExtractor
from src.extract.patreon import PatreonExtractor
from src.load.load_raw import load_raw
from src.transform.transform_youtube import transform_youtube
from src.transform.transform_twitch import transform_twitch
from src.transform.transform_patreon import transform_patreon

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOCK_FILE = BASE_DIR / ".pipeline.lock"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def acquire_lock() -> bool:
    if LOCK_FILE.exists():
        logger.warning(
            "Lock file already exists (%s). A previous run may still be in "
            "progress, or crashed without cleaning up. Skipping this run.",
            LOCK_FILE,
        )
        return False

    LOCK_FILE.write_text(datetime.now(timezone.utc).isoformat())
    return True


def release_lock() -> None:
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()


def main():
    if not acquire_lock():
        sys.exit(1)

    extractors = [YouTubeExtractor, TwitchExtractor, PatreonExtractor]
    transformers = {
        "youtube": transform_youtube,
        "twitch": transform_twitch,
        "patreon": transform_patreon,
    }

    try:
        for extractor_cls in extractors:
            source = extractor_cls.source_name
            try:
                result = extractor_cls().extract()
                n_loaded = load_raw(result)
                logger.info("Loaded %d rows into raw_%s", n_loaded, result.source)

                n_transformed = transformers[result.source]()
                logger.info("Transformed %d rows for %s", n_transformed, result.source)

            except Exception:
                # Log and continue to the next platform rather than letting
                # one failure kill the whole run.
                
                logger.exception("Pipeline step failed for source '%s'", source)

    finally:
        release_lock()


if __name__ == "__main__":
    main()