import logging
import os
from datetime import datetime
from typing import Any

import podcasts_crawler
from airflow.decorators import dag, task, task_group
from podcasts_crawler.models import Episodes, EpisodesDict, Podcast

# Define default arguments for the DAG

API_URL = os.getenv("PODCASTS_API_URL") or ""
assert API_URL != "", "PODCASTS_API_URL not set"

PODCASTINDEX_API_KEY = os.getenv("PODCAST_INDEX_API_KEY") or ""
PODCASTINDEX_API_SECRET = os.getenv("PODCAST_INDEX_API_SECRET") or ""

assert PODCASTINDEX_API_KEY != "", "PODCAST_INDEX_API_KEY not set"
assert PODCASTINDEX_API_SECRET != "", "PODCAST_INDEX_API_SECRET not set"


@dag(
    start_date=datetime(2023, 10, 20),
    # schedule_interval="@daily",
    catchup=False,
    tags=["podcasts_crawler"],
)
def podcasts_crawler_dag() -> None:
    @task
    def extract_latest_crawl_date() -> int | None:
        """get latest crawl date from database

        Returns:
            int: latest crawl date in unix timestamp
        """
        return podcasts_crawler.extract.get_latest_podcast()

    @task
    def extract_podcasts(latest_crawl_date: int) -> list:
        """get podcasts from podcastindex api

        Args:
            latest_crawl_date (int): latest crawl date in database, in unix timestamp

        Returns:
            list: list of Podcast dicts.
        """
        podcasts = podcasts_crawler.extract.get_new_podcasts(latest_crawl_date)
        if len(podcasts) > 10:
            podcasts = podcasts[:10]
        return podcasts

    @task
    def transform_podcasts(podcasts: list[dict]) -> list[dict]:
        """transform list of podcasts to Podcasts model

        Args:
            podcasts (list[dict]): list of podcasts to transform

        Returns:
            Podcasts: Podcasts model
        """
        return [
            podcast.model_dump()
            for podcast in podcasts_crawler.transform.transform_podcasts(podcasts)
        ]

    @task
    def load_podcasts_task(podcasts: list[dict]) -> bool:
        """Insert podcasts to database

        Args:
            podcasts (list): list of podcasts to insert into db
        """
        podcasts_model = [Podcast.model_validate(podcast) for podcast in podcasts]
        return podcasts_crawler.load.insert_podcasts(podcasts_model)

    @task
    def extract_new_episodes(podcast: dict) -> dict:
        """get new episodes for podcasts

        Args:
            podcasts (list): list of podcasts to get new episodes for

        Returns:
            list: list of new episodes
        """
        podcast_model = Podcast.model_validate(podcast)
        logging.info(f"extracting episodes for podcast: {podcast_model.podcast_id}")
        logging.info(f"{podcast_model.podcast_id}, {podcast_model.lastUpdate}")
        new_episodes = podcasts_crawler.extract.get_new_episodes_known_podcast(
            podcast_model.podcast_id
        )
        logging.info(f"new_episodes: {len(new_episodes)}")
        if len(new_episodes) > 5:
            new_episodes = new_episodes[:5]
        episodes = EpisodesDict(
            podcast_id=podcast_model.podcast_id, episodes=new_episodes
        )
        return episodes.model_dump()

    @task
    def transform_episodes(episodes: dict) -> dict[str, Any]:
        """transform dict of episodes to Episodes model

        Args:
            episodes (list): list of episodes to transform

        Returns:
            Episodes: Episodes model
        """

        episodes_model = EpisodesDict.model_validate(episodes)
        return podcasts_crawler.transform.transform_episodes_from_podcast(
            episodes_model.episodes, episodes_model.podcast_id
        ).model_dump()

    @task
    def load_episodes_task(episodes: dict) -> bool:
        """Insert episodes to database

        Args:
            episodes (list): list of episodes to insert into db
        """
        episodes_model = Episodes.model_validate(episodes)
        return podcasts_crawler.load.insert_episodes(episodes_model)

    @task_group
    def etl_episodes(transformed_podcast: dict) -> bool:
        episodes = extract_new_episodes(podcast=transformed_podcast)
        transformed_episodes = transform_episodes(episodes)
        return load_episodes_task(transformed_episodes)

    latest_crawl_date = extract_latest_crawl_date()
    extracted_podcasts = extract_podcasts(latest_crawl_date)
    transformed_podcasts = transform_podcasts(extracted_podcasts)
    # get new episodes for the new podcasts
    load_podcasts_task(transformed_podcasts)
    etl_episodes.expand(transformed_podcast=transformed_podcasts)


podcasts_crawler_dag()
