from abc import ABCMeta, abstractmethod, abstractstaticmethod
from typing import List

import requests
from bs4 import BeautifulSoup

from anime_cli.anime import Anime


class SearchApi(metaclass=ABCMeta):
    def __init__(self, mirror: str):
        self.url = f"https://gogoanime.{mirror}"

    def get_soup(self, location: str) -> BeautifulSoup:
        """Gets soup of a page
        The get_soup function takes in the location of
        the page and the gets the html from it
        and parses the html to `BeautifulSoup`

        Args:
            location: the location of the page

        Returns:
            `BeautifulSoup` object by parsing the html

        """
        r = requests.get(f"{self.url}/{location}")
        return BeautifulSoup(r.content, features="html5lib")

    @abstractstaticmethod
    def get_headers() -> dict[str, str]:
        """Headers to set while quering anything from the site

        Returns:
            The header to set while quering anything.
            Some links require some additional headers
            to be passed to work properly
        """
        pass

    @abstractmethod
    def search_anime(self, keyword: str) -> List[Anime]:
        """Search anime searches for animes by looking at the keyword

        Args:
            keyword: The keyword to search for when searching animes

        Returns:
            A list of `Anime` that matched the keyword
        """
        pass

    @abstractmethod
    def get_episodes_count(self, anime: Anime) -> int:
        """Get the total number of episodes in an anime

        Args:
            anime: The anime for which you want to get episodes for

        Returns:
            The total number of episodes in the anime
        """
        pass

    @abstractmethod
    def get_embed_video(self, anime: Anime, episode: int) -> str:
        """Get the link to the page where the episode video is embedded

        Args:
            anime: The anime you want to get episodes for
            episode: The episode number of the anime

        Returns:
            The link to the page where the episode for the anime
            is embedded
        """
        pass

    @abstractmethod
    def get_video_url(self, embed_url: str) -> str:
        """Get the direct url to the video

        Args:
            embed_url: The link to the page where the video is embedded

        Returns:
            The direct link to the video
        """
        pass
