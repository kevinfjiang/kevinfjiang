import shutil

import yaml
from config import PATH, SUBMOD
from dateutil import parser
from mdutils import MdUtils

with open(PATH / "projects.yml") as projects:
    project_info = yaml.load(projects, Loader=yaml.FullLoader)

with open(PATH / "service.yml") as service:
    service_info = yaml.load(service, Loader=yaml.FullLoader)


def update_github_projects(mdReadMe):
    readme_table = ["Project*", "Description", "Time", "Technology"]
    cols = "description", "date", "technology"
    mdReadMe.new_line("</details>\n")

    for row in sorted(
        project_info["projects"], key=lambda en: parser.parse(en["date"]), reverse=True
    ):
        readme_table.extend([f"[{row['title']}]({row.get('code')})", *(row[val] for val in cols)])

    mdReadMe.new_line("<details><summary>projectupdate.db</summary>\n")
    mdReadMe.new_table(
        columns=4,
        rows=len(project_info["projects"]) + 1,
        text=readme_table,
        text_align="center",
    )
    mdReadMe.new_line("</details>")


def update_website_projects():
    shutil.copy(PATH / "projects.yml", SUBMOD / "_data")


def format_services(services: list[str]) -> list[str]:
    return sorted(services, key=lambda en: parser.parse(en, fuzzy=True), reverse=True)


def update_website_services():
    serve = MdUtils(str(SUBMOD / "_includes" / "services.md"))
    serve.new_line("## Services")
    for entry, services in service_info.items():
        serve.new_line(f"#### {entry}")
        serve.new_list(format_services(services))
    serve.create_md_file()
