import webbrowser
from InquirerPy import inquirer

from anicli import Anime
from anicli.search import get_embed_video, get_episode_link, get_episodes, search_anime

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
    "Stream on browser": 0,
    "Stream on a video player": 1,
    "Download the video": 2
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
    if action == 1:
        # TODO
        return
    if action == 2:
        # TODO
        return

def main():
    episode = episode_prompt(anime_prompt())
    action = action_prompt()
    embed_video = get_embed_video(episode)
    execute_action(action, embed_video)

if __name__ == "__main__":
    main()
