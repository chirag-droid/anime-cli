import subprocess as sp
import webbrowser

from InquirerPy import inquirer

from . import video_player
from .anime import Anime
from .search import (get_embed_video, get_episode_link, get_episodes_count,
                     get_video_url, search_anime)


def anime_prompt() -> Anime:
    """
    Prompts the user for the keyword then runs a search on the keyword
    And then prompts the user again from the search results and return the Anime
    """
    # Prompt the user for anime keyword
    keyword: str = inquirer.text(
        message="What anime would you like to watch?"
    ).execute()

    # Search for the animes using the keyword
    animes = search_anime(keyword)
    # Prompt the user to choose from one of the animes
    return inquirer.select(
        message=f"Found {len(animes)} results for {keyword}", choices=animes
    ).execute()


def episode_prompt(anime: Anime) -> str:
    """
    Prompts the user for the episode number to watch
    """
    # Get the total episodes count for the anime
    episodes = get_episodes_count(anime)
    # prompt the user to choose from 1 to total number of episodes
    return inquirer.text(
        message=f"Choose from 1-{episodes} episodes:",
        filter=lambda episode: get_episode_link(anime, int(episode)),
        validate=lambda episode: 1 <= int(episode) <= episodes,
    ).execute()


# A dict of actions the user can perform
actions = {
    "Stream on browser (Not recommended)": 0,
    "Stream on a video player (Recommended)": 1,
    "Download the video (TODO)": 2,
}


def action_prompt():
    """
    Prompt the user to select between the action
    he wants to do whether to stream or download
    """
    return inquirer.select(
        message="What do you want to do with the episode", choices=list(actions.keys())
    ).execute()


def execute_action(action: str, embed_video):
    """
    Execute action takes the url where the video for
    the show is embedded and performs action based on user response
    """
    action = actions[action]

    # Open the embedded video directly (which can contain ads)
    if action == 0:
        return webbrowser.open(embed_video)

    # If user wants to download or stream the video
    # get the direct url to the video
    video_url = get_video_url(embed_video)

    # Open the video url directly to a video url
    if action == 1:
        print("It might take some time for your video player to open.")
        sp.Popen(
            [video_player, f"--http-header-fields=Referer: {embed_video}", video_url]
        )
        return

    if action == 2:
        print("Not implemented yet")
        return


def continue_prompt(anime: Anime) -> str:
    """
    Prompts the user whether he want to exit from the program
    """
    return inquirer.select(
        message=f"Currently playing {anime.title}...", choices=["exit"]
    ).execute()


def main():
    anime = anime_prompt()
    episode = episode_prompt(anime)
    action = action_prompt()

    embed_video = get_embed_video(episode)
    execute_action(action, embed_video)

    running = True
    while running:
        if continue_prompt(anime) == "exit":
            running = False


if __name__ == "__main__":
    main()
