import re
from typing import List

import requests

from anime_cli.anime import Anime
from anime_cli.search import SearchApi


class GogoAnime(SearchApi):
    def __init__(self, mirror: str):
        super().__init__(mirror)

    @staticmethod
    def get_headers() -> dict[str, str]:
        return {"Referer": "https://goload.one/"}

    def search_anime(self, keyword: str) -> List[Anime]:
        # Get and parse the html from the site
        soup = self.get_soup(f"search.html?keyword={keyword}")

        # Find all the p tags which have the name class
        animes = soup.findAll("p", {"class": "name"})
        return [
            Anime(anime.a["title"], anime.a["href"].split("/")[2]) for anime in animes
        ]

    def get_episodes_count(self, anime: Anime) -> int:
        soup = self.get_soup(f"category/{anime.id}")

        # Find all the ul tag which have an id of episode_page
        episode_page = soup.find("ul", {"id": "episode_page"})
        # From the ul tag find all the elements having li tag and then get ep_end
        # from the last li tag which is the total number of episodes
        episode_count = int(episode_page.find_all("li")[-1].a["ep_end"])
        return episode_count

    def get_embed_video(self, anime: Anime, episode: int) -> str:
        soup = self.get_soup(f"{anime.id}-episode-{episode}")

        # In the html search for a `a` tag
        # having the rel: 100 and href: # properties
        link = soup.find("a", {"href": "#", "rel": "100"})
        return f'https:{link["data-video"]}'

    def get_video_url(self, embed_url: str) -> str:
        """
        Get video url returns the direct link to video by parsing
        the page where the video is embedded
        """
        # Get the page where the video is embedded
        r = requests.get(embed_url)

        # Search for the link to the video and return it
        link = re.search(r"\s*sources.*", r.text).group()
        link = re.search(r"https:.*(m3u8)|(mp4)", link).group()
        return link
