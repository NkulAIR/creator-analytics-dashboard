"""
Shared contract every source extractor follows.

Keeping this consistent across YouTube / Shopify / Patreon means the
load layer and orchestration layer don't need to know which source
they're dealing with -- they just call .extract() and get records back.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable


@dataclass
class ExtractResult:
    source: str
    extracted_at: datetime
    records: list[dict[str, Any]] = field(default_factory=list)


class BaseExtractor(ABC):
    """
    Subclass this for each platform. Implement extract() to return
    an ExtractResult. Prefer incremental pulls (e.g. "since last run")
    once the full pull is working -- see fetch_since().
    """

    source_name: str = "base"

    @abstractmethod
    def extract(self, since: datetime | None = None) -> ExtractResult:
        """Pull records from the platform API.

        Args:
            since: only fetch records updated/created after this
                timestamp. None means a full historical pull.
        """
        raise NotImplementedError

    def paginate(self, fetch_page_fn, **kwargs) -> Iterable[dict]:
        """Generic pagination helper -- override per-source if the
        API's pagination scheme doesn't fit (cursor vs offset vs page)."""
        raise NotImplementedError
