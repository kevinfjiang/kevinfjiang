import yaml
from config import PATH, SUBMOD
from mdutils import MdUtils

from update.aboutme import about_info
from update.user import user_info

with open(PATH / "informalbio.yml") as informal:
    inform = yaml.load(informal, Loader=yaml.FullLoader)


def update_github_informal(mdReadMe):
    mdReadMe.write("<details><summary>informalbio.html</summary>\n")
    mdReadMe.write(f'<p align=center><img src={inform["404img"]}></p>\n', wrap_width=0)
    mdReadMe.write(f'<p align="center"> {inform["quote"]}</p> \n', wrap_width=0)
    mdReadMe.write(f'<p align="left"> {inform["aboutme_bio"]}</p> \n', wrap_width=0)

    mdReadMe.new_line("</details>\n")


def update_website_informal():
    print("Updating website index")
    mdindex = MdUtils(
        file_name=f"{SUBMOD}/index.md",
        title=f"---\nlayout: about\ntitle: {user_info.get('Full Name', '')}\ninvisible: True\n---\n",
    )

    mdindex.title = mdindex.title[1:].replace("=", "")
    mdindex.new_line(user_info["description"])
    mdindex.new_line(user_info["extended"])

    lang = about_info["software"]["Languages"]
    inter = about_info["interests"]
    mdindex.new_line(f"\nMy top languages are {', '.join(lang[:-1])}, and {lang[-1]}.")
    mdindex.new_line(
        f"My current interests are {', '.join(inter[:-1])}, and {inter[-1]}."
    )
    mdindex.new_line(inform.get("aboutme_bio"))
    mdindex.create_md_file()

    print("Updating website 404")
    mdFour = MdUtils(
        file_name=f"{SUBMOD}/404.md", title="---\nlayout: pagenotfound\n---\n"
    )
    mdFour.title = mdFour.title[1:].replace("=", "")

    mdFour.write(
        f'<p align=center><img src={inform["404img"]} style="max-width:300px;width:100%"></p>\n',
        wrap_width=0,
    )
    mdFour.write(inform["quote"], wrap_width=0, align="center")
    mdFour.new_line()
    mdFour.write(inform["404message"], wrap_width=0)
    mdFour.create_md_file()
