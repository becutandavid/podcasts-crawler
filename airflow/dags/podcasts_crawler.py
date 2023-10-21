import os
from datetime import datetime

import requests

import podcasts_crawler
from airflow.decorators import dag, task

# Define default arguments for the DAG

API_URL = os.getenv("PODCASTS_API_URL") or ""
assert API_URL != "", "PODCASTS_API_URL not set"

PODCASTINDEX_API_KEY = os.getenv("PODCASTINDEX_API_KEY") or ""
PODCASTINDEX_API_SECRET = os.getenv("PODCASTINDEX_API_SECRET") or ""

assert PODCASTINDEX_API_KEY != "", "PODCASTINDEX_API_KEY not set"
assert PODCASTINDEX_API_SECRET != "", "PODCASTINDEX_API_SECRET not set"

# config = {
#     "api_key": PODCASTINDEX_API_KEY,
#     "api_secret": PODCASTINDEX_API_SECRET,
# }
# index = podcastindex.init(config)


# def insert_podcasts(podcasts) -> bool:
#     """add podcasts to database

#     Args:
#         podcasts (list): list of podcast models
#     """
#     # Send a POST request to the API
#     url = os.getenv("PODCASTS_API_URL")
#     request = requests.post(f"{url}/podcasts/add_podcasts", data=json.dumps(podcasts))
#     if request.status_code == 200:
#         return True
#     return False


# def get_new_podcasts(last_updated_timestamp: int) -> list:
#     """Gets new podcasts.
#         Returns a list of dicts with new podcasts.

#     Args:
#         last_updated_timestamp (int): unix timestamp of the latest update date for
#                                         the podcast

#     Raises:
#         e: re-raised exception

#     Returns:
#         list: list of dicts with new podcasts
#     """
#     try:
#         podcasts = asyncio.run(
#             index.recentFeeds(since=last_updated_timestamp, max=1000)
#         )

#         if podcasts.get("count", 0) > 0:
#             formatted_podcasts = podcasts["items"]
#             return formatted_podcasts
#         else:
#             return []
#     except Exception as e:
#         raise e


@dag(
    start_date=datetime(2023, 10, 20),
    schedule_interval="@daily",
    catchup=False,
    tags=["podcasts_crawler"],
)
def podcasts_crawler_dag():
    @task
    def get_latest_crawl_date() -> int | None:
        """get latest crawl date from database

        Returns:
            int: latest crawl date in unix timestamp
        """
        request = requests.get(f"{API_URL}/podcasts/latest")
        crawl_date = request.json()
        if crawl_date == -1:
            return None
        return crawl_date

    @task
    def get_podcasts(latest_crawl_date: int) -> list:
        """get podcasts from podcastindex api

        Args:
            latest_crawl_date (int): latest crawl date in database, in unix timestamp

        Returns:
            list: list of Podcast objects.
        """
        podcasts = podcasts_crawler.get_new_podcasts(latest_crawl_date)
        return podcasts

    @task
    def insert_podcasts_task(podcasts):
        """Insert podcasts to database

        Args:
            podcasts (list): list of podcasts to insert into db
        """
        podcasts_crawler.insert_podcasts(podcasts)

    latest_crawl_date = get_latest_crawl_date()

    podcasts = get_podcasts(latest_crawl_date)
    insert_podcasts_task(podcasts)


podcasts_crawler_dag()
