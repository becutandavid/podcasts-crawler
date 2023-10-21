import json
import os

import requests


def insert_podcast(podcast) -> bool:
    """add podcast to database

    Args:
        podcast (Podcast): podcast model
    """
    # Send a POST request to the API
    url = os.getenv("PODCASTS_API_URL")
    request = requests.post(f"{url}/podcasts/add_podcast", data=json.dumps(podcast))
    if request.status_code == 200:
        return True
    return False


def insert_podcasts(podcasts) -> bool:
    """add podcasts to database

    Args:
        podcasts (list): list of podcast models
    """
    # Send a POST request to the API
    url = os.getenv("PODCASTS_API_URL")
    request = requests.post(f"{url}/podcasts/add_podcasts", data=json.dumps(podcasts))
    if request.status_code == 200:
        return True
    return False


def insert_episode(episode) -> bool:
    """add episode to database

    Args:
        episode (Episode): episode model
    """
    # Send a POST request to the API
    url = os.getenv("PODCASTS_API_URL")
    request = requests.post(f"{url}/episodes/add_episode", data=json.dumps(episode))
    if request.status_code == 200:
        return True
    return False


def insert_episodes(episodes) -> bool:
    """add episodes to database

    Args:
        episodes (list): list of episode models
    """
    # Send a POST request to the API
    url = os.getenv("PODCASTS_API_URL")
    request = requests.post(f"{url}/episodes/add_episodes", data=json.dumps(episodes))
    if request.status_code == 200:
        return True
    return False
