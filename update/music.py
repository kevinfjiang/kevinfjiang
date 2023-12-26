# Songs
import yaml
from config import PATH
from mdutils import MdUtils
from typer import echo

NUM_TOP_SONGS = 5
SONG_TEMPLATE = '<a href="{url}"><img src="{image}" width="540" height="64"></a>'

with open(PATH / "music.yml") as songs:
    music_info = yaml.load(songs, Loader=yaml.FullLoader)
    current = [
        "What I'm currently listening to!",
        SONG_TEMPLATE.format(**music_info["Currently Listening To"]),
    ]
    top_songs = ["Top Songs"] + [
        SONG_TEMPLATE.format(**music_info["Top Songs Template"]).format(i)
        for i in range(1, NUM_TOP_SONGS + 1)
    ]


def update_github_music(mdReadMe: MdUtils):
    echo("Updating Github music page")
    mdReadMe.new_line("<details><summary>music.db</summary>\n")
    mdReadMe.new_table(columns=1, rows=2, text=current, text_align="center")
    mdReadMe.new_table(columns=1, rows=NUM_TOP_SONGS + 1, text=top_songs, text_align="center")
    mdReadMe.new_line("</details>\n")
