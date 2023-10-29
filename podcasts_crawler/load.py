import os

import requests

from .models import EpisodeModel, Episodes, EpisodeUpload, Podcast, Podcasts

API_URL = os.getenv("PODCASTS_API_URL") or ""
assert API_URL != "", "PODCASTS_API_URL not set"


def insert_podcast(podcast: Podcast) -> bool:
    """add podcast to database

    Args:
        podcast (Podcast): podcast model
    """
    # Send a POST request to the API
    request = requests.post(
        f"{API_URL}/podcasts/add_podcast",
        json=podcast.model_dump(),
        headers={"Content-Type": "application/json"},
    )
    if request.status_code == 200:
        return True
    return False


def insert_podcasts(podcasts: list[Podcast]) -> bool:
    """add podcasts to database

    Args:
        podcasts (list): list of podcast models
    """
    # Send a POST request to the API
    upload_podcasts = Podcasts(podcasts=podcasts)
    request = requests.post(
        f"{API_URL}/podcasts/add_podcasts",
        json=upload_podcasts.model_dump(),
        headers={"Content-Type": "application/json"},
    )
    if request.status_code == 200:
        return True
    raise ValueError(f"Error inserting podcasts: {request.json()}")


def insert_episode(episode: EpisodeModel) -> bool:
    """add episode to database

    Args:
        episode (Episode): episode model
    """
    # Send a POST request to the API
    request = requests.post(
        f"{API_URL}/podcasts/add_episode",
        json=episode.model_dump(),
        headers={"Content-Type": "application/json"},
    )
    if request.status_code == 200:
        return True
    return False


def insert_episodes(episodes: Episodes) -> bool:
    """add episodes to database

    Args:
        episodes (list): list of episode models
    """
    # Send a POST request to the API
    episodes_upload = EpisodeUpload(episodes=episodes.episodes)
    request = requests.post(
        f"{API_URL}/podcasts/add_episodes",
        json=episodes_upload.model_dump(),
        headers={"Content-Type": "application/json"},
    )
    if request.status_code == 200:
        return True
    raise ValueError(f"Error inserting episodes: {request.json()}")
