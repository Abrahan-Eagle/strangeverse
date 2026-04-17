"""Zep Graph pagination: cursor-based node/edge listing with retries (incl. HTTP 429)."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from zep_cloud import ApiError, InternalServerError
from zep_cloud.client import Zep

from .logger import get_logger

logger = get_logger('strangeverse.zep_paging')

_DEFAULT_PAGE_SIZE = 100
_MAX_NODES = 2000
_DEFAULT_MAX_RETRIES = 5
_DEFAULT_RETRY_DELAY = 2.0  # seconds, doubles each retry (transient errors)
_MAX_429_RETRIES = 40  # FREE tier can throttle heavily; each wait uses Retry-After


def _retry_after_seconds(headers: dict[str, str] | None) -> float:
    """Parse Retry-After header (seconds)."""
    if not headers:
        return 30.0
    lowered = {str(k).lower(): v for k, v in headers.items()}
    raw = lowered.get("retry-after")
    if raw is not None:
        try:
            return max(5.0, min(float(raw), 120.0))
        except (TypeError, ValueError):
            pass
    return 30.0


def _fetch_page_with_retry(
    api_call: Callable[..., list[Any]],
    *args: Any,
    max_retries: int = _DEFAULT_MAX_RETRIES,
    retry_delay: float = _DEFAULT_RETRY_DELAY,
    page_description: str = "page",
    **kwargs: Any,
) -> list[Any]:
    """Single page fetch with retries: 429 (rate limit), 5xx, and transient network errors."""
    if max_retries < 1:
        raise ValueError("max_retries must be >= 1")

    delay = retry_delay
    transient_attempt = 0
    count_429 = 0

    while True:
        try:
            return api_call(*args, **kwargs)
        except ApiError as e:
            if e.status_code == 429:
                count_429 += 1
                if count_429 > _MAX_429_RETRIES:
                    logger.error(
                        f"Zep {page_description}: 429 rate limit persists after {_MAX_429_RETRIES} waits"
                    )
                    raise
                wait = _retry_after_seconds(e.headers)
                logger.warning(
                    f"Zep {page_description}: rate limited (429), waiting {wait:.0f}s "
                    f"({count_429}/{_MAX_429_RETRIES})..."
                )
                time.sleep(wait)
                continue
            if e.status_code is not None and 500 <= e.status_code < 600:
                transient_attempt += 1
                if transient_attempt >= max_retries:
                    raise
                logger.warning(
                    f"Zep {page_description} HTTP {e.status_code}, retry in {delay:.1f}s "
                    f"({transient_attempt}/{max_retries})..."
                )
                time.sleep(delay)
                delay *= 2
                continue
            raise
        except (ConnectionError, TimeoutError, OSError, InternalServerError) as e:
            transient_attempt += 1
            if transient_attempt >= max_retries:
                logger.error(f"Zep {page_description} failed after {max_retries} attempts: {str(e)}")
                raise
            logger.warning(
                f"Zep {page_description} attempt {transient_attempt} failed: {str(e)[:100]}, "
                f"retrying in {delay:.1f}s..."
            )
            time.sleep(delay)
            delay *= 2


def fetch_all_nodes(
    client: Zep,
    graph_id: str,
    page_size: int = _DEFAULT_PAGE_SIZE,
    max_items: int = _MAX_NODES,
    max_retries: int = _DEFAULT_MAX_RETRIES,
    retry_delay: float = _DEFAULT_RETRY_DELAY,
) -> list[Any]:
    """Fetch all nodes (cursor pagination, max max_items). Retries per page include 429 backoff."""
    all_nodes: list[Any] = []
    cursor: str | None = None
    page_num = 0

    while True:
        kwargs: dict[str, Any] = {"limit": page_size}
        if cursor is not None:
            kwargs["uuid_cursor"] = cursor

        page_num += 1
        batch = _fetch_page_with_retry(
            client.graph.node.get_by_graph_id,
            graph_id,
            max_retries=max_retries,
            retry_delay=retry_delay,
            page_description=f"fetch nodes page {page_num} (graph={graph_id})",
            **kwargs,
        )
        if not batch:
            break

        all_nodes.extend(batch)
        if len(all_nodes) >= max_items:
            all_nodes = all_nodes[:max_items]
            logger.warning(f"Node count reached limit ({max_items}), stopping pagination for graph {graph_id}")
            break
        if len(batch) < page_size:
            break

        cursor = getattr(batch[-1], "uuid_", None) or getattr(batch[-1], "uuid", None)
        if cursor is None:
            logger.warning(f"Node missing uuid field, stopping pagination at {len(all_nodes)} nodes")
            break

    return all_nodes


def fetch_all_edges(
    client: Zep,
    graph_id: str,
    page_size: int = _DEFAULT_PAGE_SIZE,
    max_retries: int = _DEFAULT_MAX_RETRIES,
    retry_delay: float = _DEFAULT_RETRY_DELAY,
) -> list[Any]:
    """Fetch all edges (cursor pagination). Retries per page include 429 backoff."""
    all_edges: list[Any] = []
    cursor: str | None = None
    page_num = 0

    while True:
        kwargs: dict[str, Any] = {"limit": page_size}
        if cursor is not None:
            kwargs["uuid_cursor"] = cursor

        page_num += 1
        batch = _fetch_page_with_retry(
            client.graph.edge.get_by_graph_id,
            graph_id,
            max_retries=max_retries,
            retry_delay=retry_delay,
            page_description=f"fetch edges page {page_num} (graph={graph_id})",
            **kwargs,
        )
        if not batch:
            break

        all_edges.extend(batch)
        if len(batch) < page_size:
            break

        cursor = getattr(batch[-1], "uuid_", None) or getattr(batch[-1], "uuid", None)
        if cursor is None:
            logger.warning(f"Edge missing uuid field, stopping pagination at {len(all_edges)} edges")
            break

    return all_edges
