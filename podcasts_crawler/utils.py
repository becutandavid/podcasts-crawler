from typing import Any


def transform_episode_json_to_db_format(episode_json: dict[str, Any]) -> dict[str, Any]:
    """transform episode json returned from podcastindex api to db format

    Args:
        episode_json (dict): dict from podcastindex api

    Returns:
        dict[str, Any]: formatted dict ready to be inserted into db
    """

    return {
        "episode_id": episode_json["id"],
        "title": episode_json["title"],
        "description": episode_json["description"],
        "duration": episode_json["duration"],
        "enclosure": {
            "length": episode_json["enclosureLength"],
            "type": episode_json["enclosureType"],
            "url": episode_json["enclosureUrl"],
        },
        "explicit": True if episode_json["explicit"] == 1 else False,
        "guid": episode_json["guid"],
        "imageURL": episode_json["image"],
        "link": episode_json["link"],
        "pubDate": episode_json["datePublished"],
        "podcastId": episode_json["feedId"],
    }
