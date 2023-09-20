import os

import podcastindex  # type: ignore

PODCASTINDEX_API_KEY = os.getenv("PODCASTINDEX_API_KEY") or ""
PODCASTINDEX_API_SECRET = os.getenv("PODCASTINDEX_API_SECRET") or ""

assert PODCASTINDEX_API_KEY != "", "PODCASTINDEX_API_KEY not set"
assert PODCASTINDEX_API_SECRET != "", "PODCASTINDEX_API_SECRET not set"

config = {
    "api_key": PODCASTINDEX_API_KEY,
    "api_secret": PODCASTINDEX_API_SECRET,
}
index = podcastindex.init(config)


async def get_new_episodes_known_podcast(
    podcast_id: int, last_updated_timestamp: int | None = None, fulltext: bool = True
) -> list:
    """Gets new episodes for a known podcast id.
        Returns a list of dicts with new episodes.

    Args:
        podcast_id (int): podcast id
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
        episodes = await index.episodesByFeedId(
            podcast_id,
            since=last_updated_timestamp,
            max_results=1000,
            fulltext=fulltext,
        )
        if episodes.get("count", 0) > 0:
            formatted_episodes = episodes["items"]
            return formatted_episodes
        else:
            return []
    except Exception as e:
        raise e


def get_new_podcasts(last_updated_timestamp: int) -> list:
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
        podcasts = index.recentFeeds(since=last_updated_timestamp, max_results=100)
        if podcasts.get("count", 0) > 0:
            formatted_podcasts = podcasts["items"]
            return formatted_podcasts
        else:
            return []
    except Exception as e:
        raise e
