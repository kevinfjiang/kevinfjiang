import io

import googleapiclient
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from mdutils import MdUtils
from typer import Typer

from update.aboutme import update_github_aboutme, update_website_aboutme
from update.config import SUBMOD
from update.informal import update_github_informal, update_website_informal
from update.music import update_github_music, update_website_music
from update.projects import update_github_projects, update_website_projects
from update.user import (
    update_github_credits,
    update_github_user,
    update_website_user,
    user_info,
)

app = Typer()


@app.callback()
def download_resume(update: bool = True):
    if not update:
        return
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

    file_id, url = user_info["curriculum"]["file_id"], SUBMOD
    creds = Credentials.from_service_account_file("secrets.json", scopes=SCOPES)
    service = build("drive", "v3", credentials=creds)

    request = service.files().export_media(fileId=file_id, mimeType="application/pdf")
    fl = service.files().get(fileId=file_id).execute()
    fh = io.FileIO(f"{url}/docs/{fl['name']}.pdf", "wb")

    downloader = googleapiclient.http.MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


@app.command()
def github():
    # Generate markdowns
    mdReadMe = MdUtils(file_name="README")
    mdReadMe.new_line(
        mdReadMe.new_inline_image(
            text="image",
            path="https://github.com/kevinfjiang/kevinfjiang/blob/main/hello_world.png",
        )
    )

    update_github_user(mdReadMe)
    update_github_aboutme(mdReadMe)
    update_github_projects(mdReadMe)
    update_github_music(mdReadMe)
    update_github_informal(mdReadMe)
    update_github_credits(mdReadMe)

    print("'README.md created!")
    mdReadMe.create_md_file()

@app.command()
def website():
    update_website_user()
    update_website_aboutme()
    update_website_projects()
    update_website_music()
    update_website_informal()


if __name__ == "__main__":
    app()
