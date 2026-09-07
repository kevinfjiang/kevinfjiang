from datetime import datetime
from pathlib import Path
from typing import Any
import yaml
from dateutil import parser
from mdutils import MdUtils

from update.config import PATH


class ReadmeData:
    """Data model representing the structured data loaded from readme_info YAML files."""

    def __init__(self, data_dir: Path | str = PATH) -> None:
        self.data_dir = Path(data_dir)
        self._user_info: dict[str, Any] = {}
        self._aboutme_info: dict[str, Any] = {}
        self._music_info: dict[str, Any] = {}
        self._news_info: dict[str, Any] = {}
        self._projects_info: dict[str, Any] = {}
        self._service_info: dict[str, Any] = {}
        self.load()

    @classmethod
    def from_dir(cls, data_dir: Path | str) -> "ReadmeData":
        """Factory method to create a ReadmeData instance from a directory."""
        return cls(data_dir)

    def load(self) -> None:
        """Load all YAML files from the specified data directory."""
        self._user_info = self._load_yaml("user.yml")
        self._aboutme_info = self._load_yaml("aboutme.yml")
        self._music_info = self._load_yaml("music.yml")
        self._news_info = self._load_yaml("news.yml")
        self._projects_info = self._load_yaml("projects.yml")
        self._service_info = self._load_yaml("service.yml")

    def _load_yaml(self, filename: str) -> dict[str, Any]:
        filepath = self.data_dir / filename
        if not filepath.exists():
            return {}
        with open(filepath, "r", encoding="utf-8") as f:
            content = yaml.load(f, Loader=yaml.FullLoader)
            return content if isinstance(content, dict) else {}

    @staticmethod
    def _parse_date_safe(date_str: str) -> datetime:
        """Safely parse a date string into a datetime object, falling back to datetime.min if parsing fails."""
        if not date_str:
            return datetime.min
        try:
            return parser.parse(date_str, fuzzy=True)
        except Exception:
            return datetime.min

    @property
    def user(self) -> dict[str, Any]:
        """User metadata dictionary."""
        return self._user_info

    @property
    def full_name(self) -> str:
        """User title or full name."""
        return self.user.get("title", self.user.get("Full Name", ""))

    @property
    def github_username(self) -> str:
        """GitHub username."""
        return self.user.get("github_username", "")

    @property
    def linkedin_username(self) -> str:
        """LinkedIn username."""
        return self.user.get("linkedin_username", "")

    @property
    def spotify_username(self) -> str:
        """Spotify username."""
        return self.user.get("spotify_username", "")

    @property
    def about_me(self) -> dict[str, Any]:
        """About Me metadata dictionary."""
        return self._aboutme_info

    @property
    def music(self) -> dict[str, Any]:
        """Music metadata dictionary."""
        return self._music_info

    @property
    def news(self) -> list[dict[str, Any]]:
        """List of raw news items."""
        return self._news_info.get("news", [])

    @property
    def news_sorted(self) -> list[dict[str, Any]]:
        """List of news items sorted reverse-chronologically by date."""
        return sorted(
            self.news,
            key=lambda en: self._parse_date_safe(str(en.get("date", ""))),
            reverse=True,
        )

    @property
    def formatted_news(self) -> list[str]:
        """List of formatted news strings ready for Markdown rendering."""
        result = []
        for entry in self.news_sorted:
            dt = self._parse_date_safe(str(entry.get("date", "")))
            formatted_date = dt.strftime("%b. %Y") if dt != datetime.min else str(entry.get("date", ""))
            raw = f"<strong>[{formatted_date}]</strong> {entry.get('description', '')}"
            if "link" in entry:
                result.append(f"[{raw}]({entry['link']})")
            else:
                result.append(raw)
        return result

    @property
    def projects(self) -> list[dict[str, Any]]:
        """List of project dictionaries."""
        return self._projects_info.get("projects", [])

    @property
    def publications(self) -> list[dict[str, Any]]:
        """List of publication dictionaries."""
        return self._projects_info.get("publications", [])

    @property
    def projects_sorted(self) -> list[dict[str, Any]]:
        """List of projects sorted reverse-chronologically by date."""
        return sorted(
            self.projects,
            key=lambda en: self._parse_date_safe(str(en.get("date", ""))),
            reverse=True,
        )

    @property
    def services(self) -> dict[str, list[str]]:
        """Categorized services with entries sorted reverse-chronologically by date."""
        formatted: dict[str, list[str]] = {}
        for category, service_list in self._service_info.items():
            if isinstance(service_list, list):
                formatted[category] = sorted(
                    service_list,
                    key=lambda en: self._parse_date_safe(str(en)),
                    reverse=True,
                )
            else:
                formatted[category] = service_list
        return formatted

    @property
    def links(self) -> dict[str, str]:
        """Social and external links dictionary."""
        email = self.user.get("email", "")
        return {
            "gmail": f"mailto:{email}",
            "email": f"mailto:{email}",
            "linkedin": f"https://www.linkedin.com/in/{self.linkedin_username}",
            "github": f"https://github.com/{self.github_username}",
            "spotify": f"https://open.spotify.com/user/{self.spotify_username}",
        }

    @property
    def badges(self) -> dict[str, str]:
        """Badge shield image URLs."""
        return {
            "linkedin": "https://img.shields.io/badge/-LinkedIn-039BE5?style=for-the-badge&logo=Linkedin&logoColor=white",
            "github": "https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white",
            "spotify": "https://img.shields.io/badge/Spotify-1ED760?&style=for-the-badge&logo=spotify&logoColor=white",
        }

    def get_badge_markdown(self, badge_name: str, md_instance: MdUtils | None = None) -> str:
        """Generate markdown link containing the shield badge image."""
        link_url = self.links.get(badge_name, "#")
        badge_url = self.badges.get(badge_name, "")

        md_helper = md_instance if md_instance is not None else MdUtils("temp")
        image_md = md_helper.new_inline_image(badge_name, badge_url)
        return md_helper.new_inline_link(link_url, text=image_md)
