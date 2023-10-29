import asyncio
import os

import podcastindex  # type: ignore
import requests

PODCASTINDEX_API_KEY = os.getenv("PODCAST_INDEX_API_KEY") or ""
PODCASTINDEX_API_SECRET = os.getenv("PODCAST_INDEX_API_SECRET") or ""
API_URL = os.getenv("PODCASTS_API_URL") or ""

assert PODCASTINDEX_API_KEY != "", "PODCASTINDEX_API_KEY not set"
assert PODCASTINDEX_API_SECRET != "", "PODCASTINDEX_API_SECRET not set"
assert API_URL != "", "PODCASTS_API_URL not set"

config = {
    "api_key": PODCASTINDEX_API_KEY,
    "api_secret": PODCASTINDEX_API_SECRET,
}
index = podcastindex.init(config)


def get_new_episodes_known_podcast(
    podcast_id: int | list[int],
    last_updated_timestamp: int | None = None,
    fulltext: bool = True,
) -> list:
    """Gets new episodes for a known podcast id.
        Returns a list of dicts with new episodes.

    Args:
        podcast_id (int | list[int]): podcast id or list of podcast ids
        last_updated_timestamp (int): unix timestamp of the latest update date for
                                        the podcast
        fulltext (bool): Default True. Whether to return fulltext in text
                            fields or first 100 chars.

    Raises:
        e: re-raised exception

    Returns:
        list: list of dicts with new episodes
    """
    try:
        episodes = asyncio.run(
            index.episodesByFeedId(
                podcast_id,
                since=last_updated_timestamp,
                max_results=1000,
                fulltext=fulltext,
            )
        )
        if episodes.get("count", 0) > 0:
            formatted_episodes = episodes["items"]
            return formatted_episodes
        else:
            return []
    except Exception as e:
        raise e


def get_new_podcasts(latest_podcast_id: int | None = None) -> list[dict]:
    """Gets new podcasts.
        Returns a list of dicts with new podcasts.

    Args:
        last_updated_timestamp (int): unix timestamp of the latest update date for
                                        the podcast

    Raises:
        e: re-raised exception

    Returns:
        list: list of dicts with new podcasts
    """
    try:
        podcasts = asyncio.run(index.newFeeds(feed_id=latest_podcast_id, max=1000))

        if podcasts.get("count", 0) > 0:
            return podcasts["feeds"]
        else:
            return []
    except Exception as e:
        raise e


def get_latest_podcast() -> int | None:
    """Get timestamp of latest podcast update in database

    Returns:
        int: timestamp of latest podcast update in database in unix timestamp
    """
    request = requests.get(f"{API_URL}/podcasts/latest_update_time")
    latest_podcast: int = request.json()
    if latest_podcast == -1:
        return None
    return latest_podcast
