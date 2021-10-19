import subprocess as sp
import sys
import threading
import webbrowser
from typing import List

from InquirerPy import inquirer

from anime_cli.anime import Anime
from anime_cli.proxy_server import proxyServer
from anime_cli.search import SearchApi
from anime_cli.search.gogoanime import GogoAnime


def run_server(searchApi: SearchApi, serverAddress):
    """Run server function creates a server for the searchApi and runs it

    Args:
        searchApi: The api to create the proxy server for
        serverAddress: The server address to bind the server to
    """
    server = proxyServer(searchApi.get_headers(), serverAddress)
    server.serve_forever()
    server.server_close()


def anime_prompt(searchApi: SearchApi) -> Anime:
    """prompts the user for the keyword and then the anime
    The function first prompts the user for the keyword to enter
    Then runs the search on the keyword using the search api,
    prompts the user again to enter the anime from the search results

    Args:
        searchApi: The search api to use to search for animes

    Returns:
        The Anime the user selected
    """
    # Prompt the user for anime keyword
    keyword: str = inquirer.text(
        message="What anime would you like to watch?"
    ).execute()

    # Search for the animes using the keyword
    animes = searchApi.search_anime(keyword)

    # Prompt the user to choose from one of the animes
    return inquirer.select(
        message=f"Found {len(animes)} results for {keyword}", choices=animes
    ).execute()


def episode_prompt(searchApi: SearchApi, anime: Anime) -> str:
    """prompts the user for the episode number to watch

    Args:
        searchApi: the search api to use
        anime: The anime whose episodes we want the user to enter

    Returns:
        returns the link to the episode page
    """
    # Get the total episodes count for the anime
    episodes = searchApi.get_episodes_count(anime)

    # prompt the user to choose from 1 to total number of episodes
    # validate function makes sure the user enter from 1 to total number of episodes
    # filter function changes the user entered number to the link
    return inquirer.text(
        message=f"Choose from 1-{episodes} episodes:",
        filter=lambda episode: searchApi.get_embed_video(anime, int(episode)),
        validate=lambda episode: 1 <= int(episode) <= episodes,
    ).execute()


def action_prompt(actions: List[str]) -> int:
    """Prompts the user for the action to execute

    Args:
        actions: The list containing the available actions

    Returns:
        The index of the action user chose from the actions
    """
    return inquirer.select(
        message="What would you like to do for me?",
        choices=actions,
        filter=lambda action: actions.index(action),
    ).execute()


def video_player_prompt() -> str:
    """Prompt the user for the video player to use

    Returns:
        The video player for streaming
    """
    # TODO: validate whether the video player exists
    return inquirer.text(
        message="Which video player would you like to use to stream?", default="mpv"
    ).execute()


def main():
    # TODO: Ability to select which search api, mirror to use
    searchApi = GogoAnime(mirror="pe")

    # Prompt the user for anime
    anime = anime_prompt(searchApi)
    # Prompt the user for episode
    embed_url = episode_prompt(searchApi, anime)

    # A list of actions the user can perform
    actions = [
        "Stream on browser (Not recommended)",
        "Stream on a video player (Recommended)",
    ]
    # Prompt the user for the action to perform
    action = action_prompt(actions)
    video_player = video_player_prompt()

    # Directly stream the embedded url maycontain ad
    if action == 0:
        webbrowser.open(embed_url)
        return

    # If user doesn't want to directly stream
    # Get the direct link to the video
    video_url = searchApi.get_video_url(embed_url)

    # Start the proxy server
    serverAddress = ("localhost", 8081)
    print(f"Starting proxy server on {serverAddress}")
    server = threading.Thread(
        target=run_server,
        args=(
            searchApi,
            serverAddress,
        ),
        daemon=True,
    )
    server.start()

    # Change the video url to use the proxy
    video_url = f"http://{serverAddress[0]}:{serverAddress[1]}/{video_url}"

    if action == 1:
        # Stream to the video player
        print("It may take some time to open the video player. Be Patient :)")
        sp.Popen([video_player, video_url])

    while True:
        try:
            choice = inquirer.select(
                message="Note: Exitting will stop the proxy server too",
                choices=["exit"],
            ).execute()
            if choice == "exit":
                print("Bye!")
                sys.exit()
        except KeyboardInterrupt:
            print("Bye!")
            sys.exit()


if __name__ == "__main__":
    main()
