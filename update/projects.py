import glob
import os
import re
from datetime import date

import requests
import yaml
from config import PATH, SUBMOD
from mdutils import MdUtils

with open(PATH / "projects.yml") as projects:
    project_info = yaml.load(projects, Loader=yaml.FullLoader)

with open(PATH / "informalbio.yml") as informal:
    inform = yaml.load(informal, Loader=yaml.FullLoader)
    NOTFOUND = [
        "No description yet :(\n",
        "I'm working hard to get more descriptions for all my projects, as well as fixing bugs!",
        f"\n\n![gif]({inform['404img']})",
    ]


def update_github_projects(mdReadMe):
    readme_table = ["Project*", "Description", "Time", "Technology"]
    mdReadMe.new_line("</details>\n")

    for row in project_info["Projects"]:
        print(f"current project {row['name']}")

        print(
            f"""current project {[f"[{row['name']}]({row.get('link')})", *(row[val.lower()] for val in readme_table[1:4])]}"""
        )
        readme_table.extend(
            [
                f"[{row['name']}]({row.get('link')})",
                *(row[val.lower()] for val in readme_table[1:4]),
            ]
        )

    mdReadMe.new_line("<details><summary>projectupdate.db</summary>\n")
    mdReadMe.new_table(
        columns=4,
        rows=len(project_info["Projects"]) + 1,
        text=readme_table,
        text_align="center",
    )
    mdReadMe.new_line("</details>")


def handle_github_link(row, mdpage):
    repo = row["link"].replace("https://github.com/", "")
    for branch in ["main", "master"]:
        print(
            f"Making request for https://raw.githubusercontent.com/{repo}/{branch}/README.md"
        )
        r = requests.get(f"https://raw.githubusercontent.com/{repo}/{branch}/README.md")
        if r:
            print(
                f"raw file found at https://raw.githubusercontent.com/{repo}/{branch}/README.md, continuing"
            )
            mdpage.write(r.text, wrap_width=0)
            break
    else:
        row["link"] = ""
        print(f"No README.md found for {row['link']}, I'm in confusion")


def update_website_projects():
    header = """\
---
layout: post
title: {name}
date: {date}
category: posts
summary: {description}
link: {link}
---
    """
    page_path = f"{SUBMOD}/_posts/"
    posts = {page.split("-")[-1][:-3]: page for page in glob.glob(f"{page_path}*")}

    for row in project_info["Projects"]:
        row = {
            "name": "Not Found",
            "date": "2022-01-01 00:00:00.000000",
            "description": "",
            "link": "",
            "key": "",
            **row,
        }

        if row["link"] is None:
            row["link"] = ""

        mdpage = MdUtils(
            file_name=page_path + str(date.today()) + "-" + row["key"],
            title=header.format(**row),
        )
        mdpage.title = mdpage.title[1:].replace("=", "")
        mdpage.new_line()

        if row["link"]:
            if "https://github.com/" in row["link"]:
                handle_github_link(row, mdpage)
        else:
            print(
                f"No link for {row['key']} found for, using: \n{row.get('web_decription', NOTFOUND)}"
            )
            if row.get("web_decription") or len(NOTFOUND) == 1:
                mdpage.write(row.get("web_decription", NOTFOUND[0]), wrap_width=0)
            else:
                mdpage.write("".join(NOTFOUND[:1]), wrap_width=0)
                mdpage.new_line(NOTFOUND[2], align="center")

        if row["key"] in posts:
            with open(posts[row["key"]], "r") as existing:
                print(f"""Old path change to '{posts[row['key']]}', no markdown created""")
                print(f"""New file '{page_path + str(date.today())+ "-" + row['key']}' """)

                if re.split("---\s+", existing.read())[-1] == re.sub(
                    "\s*", "", mdpage.file_data_text, 1
                ):
                    print(f"No change to '{row['key']}', no markdown created")
                    continue
                else:
                    print(f"Old markdown '{row['key']}' removed")
                    os.remove(posts[row["key"]])

        mdpage.create_md_file()
        print(f"New markdown '{row['key']}' created")
        print(f"""New file '{page_path+str(date.today())+"-"+row['key']}' """)
