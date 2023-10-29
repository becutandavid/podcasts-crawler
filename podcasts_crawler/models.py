from pydantic import BaseModel


class Podcast(BaseModel):
    podcast_id: int
    url: str | None = None
    title: str | None = None
    lastUpdate: int | None = None
    link: str | None = None
    lastHttpStatus: int | None = None
    dead: int | None = None
    contentType: str | None = None
    itunesId: int | None = None
    originalUrl: str | None = None
    itunesAuthor: str | None = None
    itunesOwnerName: str | None = None
    explicit: int | None = None
    imageUrl: str | None = None
    itunesType: str | None = None
    generator: str | None = None
    newestItemPubDate: int | None = None
    language: str | None = None
    oldestItemPubDate: int | None = None
    episodeCount: int | None = None
    popularityScore: int | None = None
    priority: int | None = None
    createdOn: int | None = None
    updateFrequency: int | None = None
    chash: str | None = None
    host: str | None = None
    newestEnclosureUrl: str | None = None
    podcastGuid: str | None = None
    description: str | None = None
    category1: str | None = None
    category2: str | None = None
    category3: str | None = None
    category4: str | None = None
    category5: str | None = None
    category6: str | None = None
    category7: str | None = None
    category8: str | None = None
    category9: str | None = None
    category10: str | None = None
    newestEnclosureDuration: int | None = None


class Podcasts(BaseModel):
    podcasts: list[Podcast]


class EpisodeModel(BaseModel):
    episode_id: int
    podcast_id: int
    title: str | None = None
    link: str | None = None
    description: str | None = None
    guid: str | None = None
    datePublished: int | None = None
    datePublishedPretty: str | None = None
    dateCrawled: int | None = None
    enclosureUrl: str | None = None
    enclosureType: str | None = None
    enclosureLength: int | None = None
    duration: int | None = None
    explicit: int | None = None
    episode: int | None = None
    episodeType: str | None = None
    season: int | None = None
    image: str | None = None
    feedItunesId: int | None = None
    feedImage: str | None = None
    feedId: int | None = None
    feedLanguage: str | None = None
    feedDead: int | None = None
    feedDuplicateOf: str | None = None
    chaptersUrl: str | None = None
    transcriptUrl: str | None = None


class EpisodeMinimal(BaseModel):
    title: str
    link: str
    description: str
    # datePublished: int


class EpisodesDict(BaseModel):
    podcast_id: int
    episodes: list[dict]


class Episodes(BaseModel):
    podcast_id: int
    episodes: list[EpisodeModel]


class EpisodeUpload(BaseModel):
    episodes: list[EpisodeModel]
