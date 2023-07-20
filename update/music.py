# Songs
from datetime import datetime
import re

import yaml
from config import PATH, SUBMOD
from mdutils import MdUtils

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


def update_github_music(mdReadMe):
    print("Updating Github music page")
    mdReadMe.new_line("<details><summary>music.db</summary>\n")
    mdReadMe.new_table(columns=1, rows=2, text=current, text_align="center")
    mdReadMe.new_line()
    mdReadMe.new_table(
        columns=1, rows=NUM_TOP_SONGS + 1, text=top_songs, text_align="center"
    )
    mdReadMe.new_line("</details>\n")


def update_website_music():
    print("Updating web music page")
    mdmusic = MdUtils(
        file_name=f"{SUBMOD}/menu/music.md",
        title=f"---\nlayout: post\ntitle: Music\ndate: {datetime.now()!s}\ncategory: menu \npermalink: /music/ \n---",
    )
    mdmusic.title = mdmusic.title[1:].replace("=", "")

    # Generate markdown music files
    mdmusic.new_line("\n" + music_info["Blurb"] + "\n")
    mdmusic.new_table(columns=1, rows=2, text=current, text_align="center")
    mdmusic.new_line()
    mdmusic.new_table(
        columns=1, rows=NUM_TOP_SONGS + 1, text=top_songs, text_align="center"
    )

    with open(f"{SUBMOD}/menu/music.md") as existing:
        if re.split("---\s+", existing.read())[-1] != re.sub(
            "\s*", "", mdmusic.file_data_text, 1
        ):
            print("Exact same, no update")
            mdmusic.create_md_file()
        else:
            print("Music page updated")
