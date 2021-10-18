import subprocess as sp
import threading
import webbrowser

from InquirerPy import inquirer

from anime_cli.prompts import Prompts
from anime_cli.proxy_server import proxyServer
from anime_cli.search import SearchApi
from anime_cli.search.gogoanime import GogoAnime


def run_server(searchApi: SearchApi, serverAddress):
    server = proxyServer(searchApi.get_headers(), serverAddress)
    server.serve_forever()


def prompt_episode(searchApi: SearchApi):
    prompts = Prompts(searchApi)

    # Prompt the user for anime
    anime = prompts.anime_prompt()
    # Prompt the user for episode
    return prompts.episode_prompt(anime)


def main():
    # TODO: Ability to select which search api, mirror to use
    searchApi = GogoAnime(mirror="pe")
    # A list of actions the user can perform
    embed_url = prompt_episode(searchApi)
    actions = [
        "Stream on browser (Not recommended)",
        "Stream on a video player (Recommended)",
    ]

    # Prompt the user for which action to do
    # download or stream
    action = inquirer.select(
        message="What would you like to do for me?",
        choices=actions,
        filter=lambda action: actions.index(action),
    ).execute()

    video_player = inquirer.text(
        message="Which video player would you like to use to stream?", default="mpv"
    ).execute()

    # Directly stream the embedded url maycontain ad
    if action == 0:
        webbrowser.open(embed_url)
        return

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
    )
    server.start()

    # Change the video url to use the proxy
    video_url = f"http://{serverAddress[0]}:{serverAddress[1]}/{video_url}"

    if action == 1:
        # Stream to the video player
        sp.Popen([video_player, video_url])
        return


if __name__ == "__main__":
    main()
