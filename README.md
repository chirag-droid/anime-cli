## AniCli

A CLI for streaming, downloading anime shows.
The shows data is indexed through [GogoAnime](https://gogoanime.pe).

> Currently only supports streaming to browser, more features coming soon.

https://user-images.githubusercontent.com/81347541/137595104-0c0418e9-71b8-4c45-b507-78892cca961c.mp4

### Installation
You can install anicli from pip

 using
```
pip install anicli
```
Then run using `python -m anicli` or simply `anicli`

If you want to help develop `anicli`. It is recommended that you clone the repo using and then install the dependencies
```
git clone https://github.com/chirag-droid/anicli.git
poetry install
```
and then to run, `poetry run anicli`

### Motivation

I recently found out about [ani-cli](https://github.com/pystardust/ani-cli), but it was not cross-platform because it was written in shell, so I decided to recreate that same thing in Python, hoping to make it cross-platform and possibly also have pretty UI.

### TODO
- [x] Stream on browser
- [ ] Stream to video players like VLC, MPV
- [ ] Ability to download the shows
- [ ] Support for multiple mirrors
- [ ] ~~Support for multiple sites~~
