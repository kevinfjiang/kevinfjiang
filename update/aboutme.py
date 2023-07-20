import yaml
from config import PATH, SUBMOD
from mdutils import MdUtils

from update.user import button_templates, user_info

with open(PATH / "aboutme.yml") as aboutme:
    about_info = yaml.load(aboutme, Loader=yaml.FullLoader)

ALT_BADGES = [
    button_templates[key].format(user_info[key])
    for key in ["github_username", "spotify_username"]
]


def update_github_aboutme(mdReadMe):
    # Update about me
    print("Updating aboutme section GitHub")
    mdReadMe.new_line("<details><summary>aboutme.py</summary>")
    mdReadMe.new_line("<blockquote>\n")
    mdReadMe.new_line("```python")
    mdReadMe.new_line("class KevinFJiang(ReadMe, GitHub):")
    mdReadMe.new_line("\tdef __init__(self):\n")

    for tag, val in about_info.items():
        if isinstance(val, str):
            mdReadMe.write(f"\t\tself.{tag} = '{val}'\n", wrap_width=0)
        elif isinstance(val, dict):
            mdReadMe.write(f"\n\t\tself.{tag} = {{\n", wrap_width=0)
            for k, v in val.items():
                if isinstance(v, list):
                    mdReadMe.write(f"\t\t\t'{k}': {v},\n", wrap_width=0)
                elif isinstance(v, str):
                    mdReadMe.write(f"\t\t\t'{k}': '{v}',\n", wrap_width=0)
            mdReadMe.write("\t\t}\n")
        elif isinstance(val, list):
            mdReadMe.write(f"\t\tself.{tag} = [\n", wrap_width=0)
            for i in range(0, len(val), 2):
                mdReadMe.write(
                    f"""\t\t\t'{"', '".join(val[i:i + 2])}',\n""", wrap_width=0
                )
            mdReadMe.write("\t\t]\n", wrap_width=0)

    mdReadMe.new_line("\tdef view(self, request, *args, **kwargs):\n")
    mdReadMe.new_line("\t\treturn self.render(request, *args, **kwargs)\n")
    mdReadMe.new_line("```")
    mdReadMe.new_line('<p align = "middle">')

    for button in ALT_BADGES:
        mdReadMe.new_line(button)

    mdReadMe.new_line("</blockquote></details>")
    print("Done updating aboutme section GitHub")


def update_website_aboutme():
    print("Updating aboutme section web")
    mdabout = MdUtils(
        file_name=f"{SUBMOD}/About Me.md",
        title="---\nlayout: about\ntitle: About Me\npermalink: /aboutme/\n---\n",
    )
    mdabout.title = mdabout.title[1:].replace("=", "")
    mdabout.new_line()

    mdabout.write("### More About me: \n")
    mdabout.write(
        about_info["bio"] + "\n\n",
    )
    mdabout.write(f"![Schrodinger's Cat]({about_info['img']})\n", wrap_width=0)

    mdabout.create_md_file()
