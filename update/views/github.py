from datetime import datetime
from pathlib import Path
import requests
from mdutils import MdUtils
from typer import echo

from update.models import ReadmeData
from update.views.base import BaseView


class GithubView(BaseView):
    """View responsible for rendering and creating the GitHub README file."""

    NUM_TOP_SONGS = 5
    SONG_TEMPLATE = '<a href="{url}"><img src="{image}" width="540" height="64"></a>'

    def __init__(
        self,
        data: ReadmeData,
        file_name: str | Path = "README",
        output_dir: str | Path | None = None,
    ) -> None:
        super().__init__(data)
        file_path = Path(file_name)
        if output_dir:
            file_path = Path(output_dir) / file_path.name

        if file_path.suffix.lower() == ".md":
            self.file_name = str(file_path.with_suffix(""))
        else:
            self.file_name = str(file_path)

    def render_header(self, md: MdUtils) -> None:
        """Render header image."""
        md.new_line(md.new_inline_image(text="image", path="hello_world.png"))

    def render_user_section(self, md: MdUtils) -> None:
        """Render user badge row and description."""
        badges_text = " ".join(
            self.data.get_badge_markdown(b, md_instance=md)
            for b in ("github", "linkedin", "spotify")
        )
        md.write(f'<p align="center">{badges_text}</p>')
        md.new_line(self.data.about_me.get("description", ""))
        echo("GitHub user section updated")

    def render_projects_section(self, md: MdUtils) -> None:
        """Render project table wrapped in collapsible details tag."""
        readme_table = ["Project*", "Description", "Time", "Technology"]
        cols = ("description", "date", "technology")

        sorted_projects = self.data.projects_sorted
        for row in sorted_projects:
            title_md = f"[{row['title']}]({row.get('code', '#')})"
            readme_table.extend([title_md, *(str(row.get(val, "")) for val in cols)])

        md.new_line("<details><summary>projectupdate.db</summary>\n")
        md.new_table(
            columns=4,
            rows=len(sorted_projects) + 1,
            text=readme_table,
            text_align="center",
        )
        md.new_line("</details>")

    def render_music_section(self, md: MdUtils) -> None:
        """Render Spotify listening tables wrapped in collapsible details tag."""
        echo("Updating Github music page")
        music_info = self.data.music
        current_data = music_info.get("Currently Listening To", {})
        top_template = music_info.get("Top Songs Template", {})

        current_table = [
            "What I'm currently listening to!",
            self.SONG_TEMPLATE.format(
                url=current_data.get("url", ""), image=current_data.get("image", "")
            ),
        ]

        top_songs_table = ["Top Songs"] + [
            self.SONG_TEMPLATE.format(
                url=top_template.get("url", "").format(i),
                image=top_template.get("image", "").format(i),
            )
            for i in range(1, self.NUM_TOP_SONGS + 1)
        ]

        md.new_line("<details><summary>music.db</summary>\n")
        md.new_table(columns=1, rows=2, text=current_table, text_align="center")
        md.new_table(
            columns=1,
            rows=self.NUM_TOP_SONGS + 1,
            text=top_songs_table,
            text_align="center",
        )
        md.new_line("</details>\n")

    def render_informal_section(self, md: MdUtils) -> None:
        """Render informal bio gif inside collapsible details tag."""
        md.new_line("<details><summary>informalbio.html</summary>\n")
        gif_url = self.data.about_me.get("gif", "")
        md.new_line(MdUtils.new_inline_image("gif", gif_url))
        md.new_line("</details>")

    def render_credits_section(self, md: MdUtils) -> None:
        """Render credits and repository metadata section."""
        md.new_line("-----\n")
        md.new_line(f"AUTHOR: {self.data.full_name}\n")
        md.new_line(
            "CREDITS: [Kevin F. Jiang](github.com/kevinfjiang). [Gabriel Alcaras](https://gaalcaras.com/en/), [Maarten Grootendors](https://github.com/MaartenGr), and [Nate Moore](https://github.com/natemoo-re).\n"
        )
        echo("making request for creation date to repo")
        created_date = self._fetch_creation_date()
        if created_date:
            md.new_line(f"CREATED: {created_date}\n")
        md.new_line(f"LAST UPDATED: {datetime.now().strftime('%b %-d, %Y')}")
        echo("finalizing credits to github")

    def _fetch_creation_date(self) -> str | None:
        username = self.data.github_username
        if not username:
            return None
        try:
            url = f"https://api.github.com/repos/{username}/{username}"
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                raw_date = resp.json().get("created_at")
                if raw_date:
                    dt = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ")
                    return dt.strftime("%b %-d, %Y")
        except Exception as err:
            echo(f"Warning: Unable to fetch repository creation date: {err}")
        return None

    def generate(self) -> None:
        """Generate and save the complete GitHub README markdown file."""
        md = MdUtils(file_name=self.file_name)
        self.render_header(md)
        self.render_user_section(md)
        self.render_projects_section(md)
        self.render_music_section(md)
        self.render_informal_section(md)
        self.render_credits_section(md)

        echo(f"{self.file_name}.md created!")
        md.create_md_file()
