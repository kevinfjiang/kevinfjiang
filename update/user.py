import glob
import os
import re
from datetime import datetime

import requests
import yaml
from config import PATH, SUBMOD

link_dict = {  # add more as needed
    "gmail": "mailto:{0}",
    "email": "mailto:{0}",
    "linkedin": "https://www.linkedin.com/in/{0}",
    "github": "https://github.com/{0}",
    "spotify": "https://open.spotify.com/user/{0}",
}

button_templates = {
    "email": f'<a href={link_dict["gmail"]}" target="blank"><img align="center" src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" /></a>',
    "linkedin_username": f'<a href={link_dict["linkedin"]} target="blank"><img align="center" src="https://img.shields.io/badge/-LinkedIn-039BE5?style=for-the-badge&logo=Linkedin&logoColor=white"/></a>',
    "curriculum": '<a href="{}" align="center" target="blank"><img align="center" src="https://img.shields.io/badge/resume-built-green?style=for-the-badge" /></a>',
    "github_username": f'<a href="{link_dict["github"]}?tab=repositories" target="blank"><img align="center" src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" /></a>',
    "spotify_username": f'<a href={link_dict["spotify"]} target="blank"><img align="center" src="https://img.shields.io/badge/Spotify-1ED760?&style=for-the-badge&logo=spotify&logoColor=white" /></a>',
}


with open(PATH / "user.yml") as user:
    user_info = yaml.load(user, Loader=yaml.FullLoader)


def find_recent_resume(url) -> str:
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


def update_github_user(mdReadMe):
    print("GitHub user section updated")
    mdReadMe.new_line('<p align="center">')
    for key in ["email", "linkedin_username", "curriculum"]:
        mdReadMe.write("\n")
        if key == "curriculum":
            info = os.path.join(f"https://{SUBMOD}/docs/", find_recent_resume(SUBMOD))
        else:
            info = user_info[key]
        mdReadMe.write(button_templates[key].format(info), wrap_width=0)
    mdReadMe.write("</p>")

    mdReadMe.new_line(f"{user_info['description']} {user_info['extended']}")


def update_website_user():
    print("website user section updated")
    with open(f"{SUBMOD}/config_base.yml") as static:
        under_config = {**user_info, **yaml.load(static, Loader=yaml.FullLoader)}

    resume_url = os.path.join("/docs/", find_recent_resume(SUBMOD))
    user_info["curriculum"]["url"] = resume_url

    with open(f"{SUBMOD}/_config.yml", "w") as dest:
        documents = yaml.dump(under_config, dest)
    return documents


def update_github_credits(mdReadMe):
    print("finalizing credits to github")
    mdReadMe.new_line("-----\n")
    mdReadMe.new_line(f"AUTHOR: {user_info.get('Full Name', '')}\n")
    mdReadMe.new_line(
        "CREDITS: [Kevin F. Jiang](github.com/kevinfjiang). [Gabriel Alcaras](https://gaalcaras.com/en/), [Maarten Grootendors](https://github.com/MaartenGr), and [Nate Moore](https://github.com/natemoo-re).\n"
    )
    print("making request for creation date to repo")
    created = requests.get(
        f"""https://api.github.com/repos/{user_info.get('github_username')}/{user_info.get('github_username')}"""
    ).json()["created_at"]
    mdReadMe.new_line(
        f"""CREATED: {datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ").strftime("%b %-d, %Y")}\n"""
    )
    mdReadMe.new_line(f"LAST UPDATED: {datetime.now().strftime('%b %-d, %Y')}")
