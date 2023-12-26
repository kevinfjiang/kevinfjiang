import glob
import re
from datetime import datetime

import requests
import yaml
from config import PATH, SUBMOD
from mdutils import MdUtils
from typer import echo

with open(PATH / "user.yml") as user, open(PATH / "aboutme.yml") as aboutme:
    user_info = yaml.load(user, Loader=yaml.FullLoader)
    aboutme_info = yaml.load(aboutme, Loader=yaml.FullLoader)

links = {  # add more as needed
    "gmail": "mailto:{0}",
    "email": "mailto:{0}",
    "linkedin": f"https://www.linkedin.com/in/{user_info['linkedin_username']}",
    "github": f"https://github.com/{user_info['github_username']}",
    "spotify": f"https://open.spotify.com/user/{user_info['spotify_username']}",
}

badges = {
    "linkedin": "https://img.shields.io/badge/-LinkedIn-039BE5?style=for-the-badge&logo=Linkedin&logoColor=white",
    "github": "https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white",
    "spotify": "https://img.shields.io/badge/Spotify-1ED760?&style=for-the-badge&logo=spotify&logoColor=white",
}


def find_recent_resume(url: str) -> str:
    season_dict = {"W": 4, "F": 3, "X": 2, "S": 1}
    match = re.compile(r"""([0-9]{2})([a-zA-Z])""")

    def recent_sort(path):
        year, season = re.search(match, path).groups()
        return year, season_dict.get(season)

    path = max(
        (r.split("/docs/")[1] for r in glob.glob(f"./{url}/docs/Resume_*.pdf")),
        key=recent_sort,
    )
    return path


def update_github_informal(mdReadMe: MdUtils):
    mdReadMe.new_line("<details><summary>informalbio.html</summary>\n")
    mdReadMe.new_line(MdUtils.new_inline_image("gif", aboutme_info["gif"]))
    mdReadMe.new_line("</details>")


def badge_helper(badge_name: str) -> str:
    image = MdUtils.new_inline_image(badge_name, badges[badge_name])
    return MdUtils.new_inline_link(links[badge_name], image)


def update_github_user(mdReadMe: MdUtils):
    badges_text = " ".join(badge_helper(b) for b in ("github", "linkedin", "spotify"))
    mdReadMe.write(f"""<p align="center">{badges_text}</p>""")
    mdReadMe.new_line(aboutme_info["description"])
    echo("GitHub user section updated")


def update_website_user():
    # Updates aboutme section
    aboutme = MdUtils(file_name=str(SUBMOD / "_includes" / "aboutme.md"))
    aboutme.new_line("## About Me")
    aboutme.new_line(aboutme_info["description"])
    aboutme.create_md_file()

    with open(SUBMOD / "config_base.yml") as base, open(SUBMOD / "_config.yml", "w") as conf:
        web_config = {**user_info, **yaml.load(base, Loader=yaml.FullLoader)}
        yaml.dump(web_config, conf)

    echo("website user section updated")


def update_github_credits(mdReadMe):
    mdReadMe.new_line("-----\n")
    mdReadMe.new_line(f"AUTHOR: {user_info.get('Full Name', '')}\n")
    mdReadMe.new_line(
        "CREDITS: [Kevin F. Jiang](github.com/kevinfjiang). [Gabriel Alcaras](https://gaalcaras.com/en/), [Maarten Grootendors](https://github.com/MaartenGr), and [Nate Moore](https://github.com/natemoo-re).\n"
    )
    echo("making request for creation date to repo")
    created = requests.get(
        f"""https://api.github.com/repos/{user_info.get('github_username')}/{user_info.get('github_username')}"""
    ).json()["created_at"]
    mdReadMe.new_line(
        f"""CREATED: {datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ").strftime("%b %-d, %Y")}\n"""
    )
    mdReadMe.new_line(f"LAST UPDATED: {datetime.now().strftime('%b %-d, %Y')}")
    echo("finalizing credits to github")
