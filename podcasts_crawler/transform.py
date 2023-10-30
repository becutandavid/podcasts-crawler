from .models import EpisodeModel, Episodes, Podcast


def transform_podcast(podcast: dict) -> Podcast:
    """transform podcast dict to Podcast model

    Args:
        podcast (dict): dict from podcastindex api

    Returns:
        Podcast: Podcast model suitable for database insertion
    """
    podcast["podcast_id"] = podcast.pop("id")
    podcast["newestItemPubDate"] = podcast.pop("newestItemPublishTime")
    podcast["oldestItemPubDate"] = podcast.pop("oldestItemPublishTime")
    if podcast.get("lastUpdate", None) is None:
        podcast["lastUpdate"] = podcast["newestItemPubDate"]
    podcast["imageUrl"] = podcast.pop("image")
    for idx, category in enumerate(podcast["categories"]):
        podcast[f"category{idx+1}"] = podcast["categories"][category]
    podcast.pop("categories")

    return Podcast(**podcast)


def transform_podcasts(podcasts: list[dict]) -> list[Podcast]:
    """transfrom list of podcast dicts to Podcasts model

    Args:
        podcasts (list[dict]): list of podcast dicts

    Returns:
        Podcasts: Podcasts model suitable for database insertion
    """
    return [transform_podcast(podcast) for podcast in podcasts]


def transform_episode(episode: dict, podcast_id: int) -> EpisodeModel:
    """transform episode dict to Episode model

    Args:
        episode (dict): dict from podcastindex api

    Returns:
        Episode: Episode model suitable for database insertion
    """
    episode["episode_id"] = episode.pop("id")
    episode["podcast_id"] = podcast_id

    return EpisodeModel(**episode)


def transform_episodes_from_podcast(episodes: list[dict], podcast_id: int) -> Episodes:
    """transform list of episode dicts to Episodes model

    Args:
        episodes (list[dict]): list of episode dicts

    Returns:
        Episodes: Episodes model suitable for database insertion
    """
    return Episodes(
        podcast_id=podcast_id,
        episodes=[transform_episode(episode, podcast_id) for episode in episodes],
    )
