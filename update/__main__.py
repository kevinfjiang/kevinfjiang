import io

import googleapiclient
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from mdutils import MdUtils
from typer import Typer, echo

from update.config import SUBMOD
from update.music import update_github_music
from update.news import update_website_news
from update.projects import (update_github_projects, update_website_projects,
                             update_website_services)
from update.user import (update_github_credits, update_github_informal,
                         update_github_user, update_website_user, user_info)

app = Typer()


@app.callback()
def download_resume(update: bool = False):
    if not update:
        return
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

    file_id, file_path = user_info["curriculum"]["file_id"], SUBMOD / "assets"
    creds = Credentials.from_service_account_file("secrets.json", scopes=SCOPES)
    service = build("drive", "v3", credentials=creds)

    request = service.files().export_media(fileId=file_id, mimeType="application/pdf")
    fl = service.files().get(fileId=file_id).execute()
    fh = io.FileIO(file_path / fl["name"], "wb")

    downloader = googleapiclient.http.MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        echo("Download %d%%." % int(status.progress() * 100))
    return


@app.command()
def github():
    # Generate markdowns
    mdReadMe = MdUtils(file_name="README")
    mdReadMe.new_line(mdReadMe.new_inline_image(text="image", path="hello_world.png"))

    update_github_user(mdReadMe)
    update_github_projects(mdReadMe)
    update_github_music(mdReadMe)
    update_github_informal(mdReadMe)
    update_github_credits(mdReadMe)

    echo("README.md created!")
    mdReadMe.create_md_file()


@app.command()
def website():
    update_website_user()
    update_website_projects()
    update_website_services()
    update_website_news()
    echo("Website created!")


if __name__ == "__main__":
    app()
