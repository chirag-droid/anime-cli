from re import sub
import subprocess
import webbrowser
from InquirerPy import inquirer

from . import video_player
from .anime import Anime
from .search import *

def anime_prompt() -> Anime:
    raw_anime: str = inquirer.text(
        message="What anime would you like to watch?"
    ).execute()
    animes = search_anime(raw_anime)
    return inquirer.select(
        message=f"Found {len(animes)} results for {raw_anime}",
        choices=animes
    ).execute()

def episode_prompt(anime: Anime) -> str:
    episodes = get_episodes(anime)
    return inquirer.text(
        message=f"Choose from 1-{episodes} episodes:",
        filter=lambda episode: get_episode_link(anime, int(episode)),
        validate=lambda episode: 1 <= int(episode) <= episodes
    ).execute()

actions = {
    "Stream on browser (Not recommended)": 0,
    "Stream on a video player (Recommended)": 1,
    "Download the video (TODO)": 2
}

def action_prompt():
    return inquirer.select(
        message="What do you want to do with the episode",
        choices=list(actions.keys())
    ).execute()

def execute_action(action: str, embed_video):
    action = actions[action]

    if action == 0:
        return webbrowser.open(embed_video)

    video_url = get_video_url(embed_video)
    if action == 1:
        print("It might take some time for your video player to open.")
        subprocess.Popen(f'{video_player} --http-header-fields="Referer: {embed_video}" {video_url}')

    if action == 2:
        print("Not implemented yet")
        return

def continue_prompt(anime: Anime) -> str:
    return inquirer.select(
        message=f"Currently playing {anime.title}...",
        choices=["exit"]
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
