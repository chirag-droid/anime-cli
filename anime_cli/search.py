import re
from typing import List

import requests
from bs4 import BeautifulSoup

from . import mirror
from .anime import Anime


def search_anime(keyword: str) -> List[Anime]:
    """
    Search anime function takes in a keyword for a specific anime
    then runs the search for specific keyword and returns a list
    of animes that are found
    """
    # Get and parse the html from the site
    r = requests.get(f"{mirror}/search.html?keyword={keyword}")
    soup = BeautifulSoup(r.content, features="html5lib")

    # Find all the p tags which have the name class
    animes = soup.findAll("p", {"class": "name"})
    return [Anime(anime.a["title"], anime.a["href"].split("/")[2]) for anime in animes]


def get_episodes_count(anime: Anime) -> int:
    """
    Get episodes count function takes in as a parameter a anime
    and returns the total number of episodes the anime has
    """
    r = requests.get(f"{mirror}/category/{anime.id}")
    soup = BeautifulSoup(r.content, features="html5lib")

    # Find all the ul tag which have an id of episode_page
    episode_page = soup.find("ul", {"id": "episode_page"})
    # From the ul tag find all the elements having li tag and then get ep_end
    # from the last li tag which is the total number of episodes
    return int(episode_page.findAll("li")[-1].a["ep_end"])


def get_episode_link(anime: Anime, episode: int):
    """
    Get episode link takes the anime and the episode number as argument
    and returns a link the episode page for the given anime
    """
    return f"{mirror}/{anime.id}-episode-{episode}"


def get_embed_video(episode_url: str) -> str:
    """
    Get embed video takes the episode page and
    returns the link to the page where the video is embedded
    """
    # Get and parse the episode page
    r = requests.get(episode_url)
    soup = BeautifulSoup(r.content, features="html5lib")

    # In the html search for a `a` tag
    # having the rel: 100 and href: # properties
    link = soup.find("a", {"href": "#", "rel": "100"})
    return f'https:{link["data-video"]}'


def get_video_url(embed_url: str) -> str:
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
