import re
from typing import List

import requests

from anime_cli.anime import Anime
from anime_cli.search import SearchApi


class GogoAnime(SearchApi):
    def __init__(self, mirror: str):
        super().__init__(mirror)
        url = f"https://gogoanime.{mirror}"
        #follow for effective url
        self.url = r = requests.get(url,allow_redirects=True,headers=self.request_headers).url

    @staticmethod
    def get_headers() -> dict[str, str]:
        return {"Referer": "https://gogoplay1.com/"}

    def search_anime(self, keyword: str) -> List[Anime]:
        # Get and parse the html from the site
        soup = self.get_soup(self.url,f"search.html?keyword={keyword}")

        # Find all the p tags which have the name class
        animes = soup.findAll("p", {"class": "name"})
        return [
            Anime(anime.a["title"], anime.a["href"].split("/")[2]) for anime in animes
        ]

    def get_episodes_count(self, anime: Anime) -> int:
        soup = self.get_soup(self.url,f"category/{anime.id}")

        # Find all the ul tag which have an id of episode_page
        episode_page = soup.find("ul", {"id": "episode_page"})
        # From the ul tag find all the elements having li tag and then get ep_end
        # from the last li tag which is the total number of episodes
        episode_count = int(episode_page.find_all("li")[-1].a["ep_end"])
        return episode_count

    def get_embed_video(self, anime: Anime, episode: int) -> str:
        soup = self.get_soup(self.url,f"{anime.id}-episode-{episode}")

        # In the html search for a `a` tag
        # having the rel: 100 and href: # properties
        link = soup.find("a", {"href": "#", "rel": "100"})
        return f'https:{link["data-video"]}'

    def get_video_url(self, embed_url: str) -> str:
        """
        Get video url returns the direct link to video by parsing
        the page where the video is embedded
        """
        #get episodeid from embed_url
        episode_id_match = re.search(r"id.+?&",embed_url)
        if not episode_id_match:
            raise Exception("Cannot find episode_id from embed_url.\nembed_url: {}".format(embed_url))
        episode_id = episode_id_match.group(0)

        #get authority from embed_url
        steaming_base = re.search(r"(https://).+/",embed_url).group(0)

        find_mp4s = re.compile(r"(http|https):\/\/.*com\/cdn.*expiry=[0-9]*")
        soup = self.get_soup(steaming_base,f"/download?{episode_id}")
        mp4s = soup.find_all("a", {"href": find_mp4s})

        if (len(mp4s) == 0):
            return Exception("Cannot find mp4s in video_url.\nvideo_url: {}{}".format(steaming_base,f"/download?{episodeid}"))

        highest_quality = mp4s[len(mp4s)-1]
        return highest_quality.attrs["href"]