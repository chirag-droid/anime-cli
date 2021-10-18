from InquirerPy import inquirer

from anime_cli.anime import Anime
from anime_cli.search import SearchApi


class Prompts:
    def __init__(self, searchApi: SearchApi):
        self.searchApi = searchApi

    def anime_prompt(self) -> Anime:
        """
        Prompts the user for the keyword then runs a search on the keyword
        And then prompts the user again from the search results and return the Anime
        """
        # Prompt the user for anime keyword
        keyword: str = inquirer.text(
            message="What anime would you like to watch?"
        ).execute()

        # Search for the animes using the keyword
        animes = self.searchApi.search_anime(keyword)
        # Prompt the user to choose from one of the animes
        return inquirer.select(
            message=f"Found {len(animes)} results for {keyword}", choices=animes
        ).execute()

    def episode_prompt(self, anime: Anime) -> str:
        """
        Prompts the user for the episode number to watch
        """
        # Get the total episodes count for the anime
        episodes = self.searchApi.get_episodes_count(anime)
        # prompt the user to choose from 1 to total number of episodes
        return inquirer.text(
            message=f"Choose from 1-{episodes} episodes:",
            filter=lambda episode: self.searchApi.get_embed_video(anime, int(episode)),
            validate=lambda episode: 1 <= int(episode) <= episodes,
        ).execute()
