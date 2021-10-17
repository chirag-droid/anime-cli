from typing import List
import requests
from bs4 import BeautifulSoup
import re

from . import mirror
from .anime import Anime

def search_anime(keyword: str) -> List[Anime]:
    r = requests.get(f"{mirror}/search.html?keyword={keyword}")
    soup = BeautifulSoup(r.content, features="html5lib")
    animes = soup.findAll("p", {"class": "name"})
    return [Anime(anime.a["title"], anime.a["href"].split("/")[2]) for anime in animes]

def get_episodes(anime: Anime) -> int:
    r = requests.get(f"{mirror}/category/{anime.id}")
    soup = BeautifulSoup(r.content, features="html5lib")
    episode_page = soup.find("ul", {"id": "episode_page"})
    return int(episode_page.findAll("li")[-1].a["ep_end"])

def get_episode_link(anime: Anime, episode: int):
    return f"{mirror}/{anime.id}-episode-{episode}"

def get_embed_video(episode_url: str) -> str:
    r = requests.get(episode_url)
    soup = BeautifulSoup(r.content, features="html5lib")
    link = soup.find("a", {"href": "#", "rel": "100"})
    return f'https:{link["data-video"]}'

def get_video_url(embed_url: str) -> str:
    r = requests.get(embed_url)
    link = re.search("\s*sources.*", r.text).group()
    link = re.search("https:.*(m3u8)|(mp4)", link).group()
    return link
