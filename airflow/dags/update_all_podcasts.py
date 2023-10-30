import os
from datetime import datetime

import requests

from airflow.decorators import dag, task, task_group
from podcasts_crawler.extract import get_new_episodes_known_podcast
from podcasts_crawler.load import insert_episodes
from podcasts_crawler.models import (
    EpisodeDictsForPodcast,
    Episodes,
)
from podcasts_crawler.transform import transform_episodes_from_podcast

API_URL = os.getenv("PODCASTS_API_URL") or ""
assert API_URL != "", "PODCASTS_API_URL not set"

PODCASTINDEX_API_KEY = os.getenv("PODCAST_INDEX_API_KEY") or ""
PODCASTINDEX_API_SECRET = os.getenv("PODCAST_INDEX_API_SECRET") or ""

assert PODCASTINDEX_API_KEY != "", "PODCAST_INDEX_API_KEY not set"
assert PODCASTINDEX_API_SECRET != "", "PODCAST_INDEX_API_SECRET not set"


@dag(dag_id="load_episodes_for_all_podcasts", start_date=datetime(2023, 10, 29))
def get_episodes_for_all_podcasts():
    @task
    def generate_podcast_offset_values() -> list[dict[str, int]]:
        # get 200 podcasts. Add one by one until sum of episodes == 1000.
        # Then, remember podcast number, and offset. Get next 200 podcasts from that id.
        # Repeat. If podcasts have more than 1000 episodes, just get latest 1000.

        # After generating all limit and offset values, return them as a list of tuples.
        limit = 200
        offset = 0
        previous_offset = 0

        return_data: list[dict[str, int]] = []

        counter = 0
        while True:
            counter += 1

            if counter > 10:
                break

            response = requests.get(f"{API_URL}/podcasts?limit={limit}&offset={offset}")
            current_count = 0
            episode_count = 0
            for podcast in response.json():
                if episode_count + podcast["episodeCount"] > 1000:
                    return_data.append(
                        {"offset": previous_offset, "limit": current_count}
                    )
                    previous_offset = offset

                    break
                else:
                    episode_count += podcast["episodeCount"]
                    current_count += 1
                    offset += 1

        return return_data

    @task
    def get_podcast_ids(offset_and_limit: dict) -> int:
        offset = offset_and_limit["offset"]
        limit = offset_and_limit["limit"]
        podcast_ids = requests.get(
            f"{API_URL}/podcasts/ids?limit={limit}&offset={offset}"
        )

        return podcast_ids.json()

    @task
    def extract_episodes(podcast_ids: list[int]) -> list[dict]:
        return get_new_episodes_known_podcast(podcast_ids)

    @task
    def split_episodes_per_podcast(
        episodes: list[dict],
    ) -> list[dict]:
        formatted_episodes = {}
        for episode in episodes:
            if episode["feedId"] not in formatted_episodes:
                formatted_episodes[episode["feedId"]] = []
            formatted_episodes[episode["feedId"]].append(episode)

        output = []
        for podcast_id, episodes_iter in formatted_episodes.items():
            output.append(
                EpisodeDictsForPodcast(
                    podcast_id=podcast_id, episodes=episodes_iter
                ).model_dump()
            )
        return output

    @task
    def transform_episodes(eps: list[dict]) -> list[dict]:
        transformed_episodes = []
        for episodes in eps:
            eps_model = EpisodeDictsForPodcast.model_validate(episodes)
            transformed_episodes.append(
                transform_episodes_from_podcast(
                    eps_model.episodes, eps_model.podcast_id
                ).model_dump()
            )
        return transformed_episodes

    @task
    def load_episodes(episodes: list[dict]) -> bool:
        for eps in episodes:
            transformed_episodes = Episodes.model_validate(eps)
            if not insert_episodes(transformed_episodes):
                raise ValueError("Error inserting episodes")
        return True

    @task_group
    def etl_episodes(limit_and_offset: dict) -> bool:
        podcast_ids = get_podcast_ids(limit_and_offset)
        episodes = extract_episodes(podcast_ids)
        split_episodes = split_episodes_per_podcast(episodes)
        transformed_episodes = transform_episodes(eps=split_episodes)
        loaded_episodes = load_episodes(episodes=transformed_episodes)

        return loaded_episodes

    offset_vals = generate_podcast_offset_values()
    return etl_episodes.expand(limit_and_offset=offset_vals)


get_episodes_for_all_podcasts()
