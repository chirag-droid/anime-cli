## Anime-cli

A CLI for streaming, downloading anime shows.
The shows data is indexed through [GogoAnime](https://gogoanime.pe).

Please install [mpv video-player](https://mpv.io/installation/) for better experience and no ads.

Version 0.3.1+ works on android/Smart TV's see [usage instructions](#usage-android) below

https://user-images.githubusercontent.com/81347541/137595104-0c0418e9-71b8-4c45-b507-78892cca961c.mp4

### Usage
It's recommended to stream episodes using a video player (no ads)
Almost all video players all supported which can stream a m3u8 url. To achive this a proxy server is used.

You can install anime-cli from pip using
```
pip install anime-cli
```
Then run using `python -m anime_cli` or simply `anime-cli`

If you want to help develop `anime-cli`. It is recommended that you clone the repo using and then install the dependencies
```
git clone https://github.com/chirag-droid/anime-cli.git
poetry install
```
and then to run, `poetry run anime-cli`

### Usage Android
- Download `Termux` from Fdroid
- Download `mpv-player` from playstore

In termux install python using `pkg install python`
Follow the same steps as above for downloading `anime-cli`

When asked to enter the video-player change it to `xdg-open` which will automatically open `mpv-player`.

### Motivation

I recently found out about [ani-cli](https://github.com/pystardust/ani-cli), but it was not cross-platform because it was written in shell, so I decided to recreate that same thing in Python, hoping to make it cross-platform and possibly also have pretty UI.

### TODO
- [x] Stream on browser
- [ ] Make streaming on browsers ad free
- [x] Stream to video player like MPV
- [ ] Ability to download the shows as mp4
- [ ] Support for multiple mirrors
